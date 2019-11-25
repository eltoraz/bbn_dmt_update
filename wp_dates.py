# wp_dates.py - skeleton for dmt manipulation code
import datetime
import tkinter
from tkinter import ttk

from tkcalendar import DateEntry

import csv_ops
import dmt
import log

def correct_wp_dates(base_date):
    baq = 'BBN_WP_Dates'                        # Epicor BAQ ID to export via DMT
    head_baq = 'BBN_WP_Dates_Headers'           # job header-specific BAQ
    scratch_dir = 'scratch\\'                   # folder to write temp CSV files
    csv = scratch_dir + baq + '.csv'            # DMT-exported CSV file
    head_export_csv = scratch_dir + head_baq + '.csv'

    assm_csv = scratch_dir + 'Job_Assembly.csv'  # CSV to re-import into DMT
    dmt_assm = 'Job Assembly'                  # DMT phase for the import step

    head_csv_pre = scratch_dir + 'Job_Head_Pre.csv'     # need to run DMT import twice,
    head_csv_post = scratch_dir + 'Job_Head_Post.csv'   #  second time to re-set release flags
    dmt_head = 'Job Header'                   #  unsetting the "new job" flag

    # check that the scratch directory exists, and create it if not
    csv_ops.check_scratch(scratch_dir)

    # export the BAQ to a CSV file
    dmt.dmt_export(baq, csv)
    dmt.dmt_export(head_baq, head_export_csv)

    # read the data into this program
    data = csv_ops.import_csv(csv)
    head_export_data = csv_ops.import_csv(head_export_csv)

    log.log('job baq size:' + str(len(data)))

    # do stuff to the data
    assm_data = []
    head_data_pre = []
    head_data_post = []

    for row in head_export_data:
        head_row_pre = {}
        head_row_pre['Company'] = row['Company']
        head_row_pre['Plant'] = row['Site']
        head_row_pre['JobNum'] = row['Job Number']
        head_row_pre['PartNum'] = row['Part']
        head_row_pre['JobEngineered'] = False
        head_row_pre['JobReleased'] = False
        head_row_pre['SchedLocked'] = True
        head_row_pre['NewlyAdded_c'] = True
        head_row_pre['ChangeDescription'] = 'DMT un-engineering to change due dates'
        head_data_pre.append(head_row_pre)

        # set the parent (assembly 0) due date to the ship by date
        assm_row = {}
        assm_row['Company'] = row['Company']
        assm_row['Plant'] = row['Site']
        assm_row['JobNum'] = row['Job Number']
        assm_row['AssemblySeq'] = 0
        assm_row['PartNum'] = row['Part']
        assm_row['StartDate'] = base_date.strftime('%m/%d/%y')
        assm_row['DueDate'] = row['Ship By']
        assm_data.append(assm_row)
        
        head_row_post = {}
        head_row_post['Company'] = row['Company']
        head_row_post['Plant'] = row['Site']
        head_row_post['JobNum'] = row['Job Number']
        head_row_post['PartNum'] = row['Part']
        head_row_post['JobEngineered'] = True
        head_row_post['JobReleased'] = True
        head_row_post['SchedLocked'] = True
        head_row_post['NewlyAdded_c'] = False
        head_row_post['ChangeDescription'] = 'DMT re-engineering after changing due dates'
        head_data_post.append(head_row_post)

    for row in data:
        # perform data transformations on each row from the exported dataset
        assm_row = {}
        assm_row['Company'] = row['Company']
        assm_row['Plant'] = row['Site']
        assm_row['JobNum'] = row['Job Number']
        assm_row['AssemblySeq'] = row['Asm']
        assm_row['PartNum'] = row['Part']
        assm_row['StartDate'] = base_date.strftime('%m/%d/%y')
        assm_row['DueDate'] = (base_date + datetime.timedelta(days=int(row['Lead']))).strftime('%m/%d/%y')
        assm_data.append(assm_row)

    log.log('job pre size:' + str(len(head_data_pre)))
    log.log('job asm size:' + str(len(assm_data)))
    log.log('job post size:' + str(len(head_data_post)))

    # headers for the CSV file to import - make sure they match the mapping in the data manipulation above
    headers_asm = ['Company', 'Plant', 'JobNum', 'AssemblySeq', 'PartNum', 'StartDate', 'DueDate']
    headers_hed = ['Company', 'Plant', 'JobNum', 'PartNum', 'JobEngineered', 'JobReleased', 'SchedLocked', 'NewlyAdded_c', 'ChangeDescription']

    # export the changes to a CSV file formatted for the specified DMT phase
    csv_ops.export_csv(headers_hed, head_data_pre, head_csv_pre)
    csv_ops.export_csv(headers_asm, assm_data, assm_csv)
    csv_ops.export_csv(headers_hed, head_data_post, head_csv_post)

    # run DMT to import the changes into Epicor
    dmt.dmt_import(dmt_head, head_csv_pre)        # need to update job header first
    dmt.dmt_import(dmt_assm, assm_csv)
    dmt.dmt_import(dmt_head, head_csv_post)

if __name__ == '__main__':
    # create the UI element that displays the date picker
    root = tkinter.Tk()
    root.withdraw()
    s = ttk.Style(root)
    s.theme_use('clam')
    top = tkinter.Toplevel(root)
    ttk.Label(top, text='Pick base date').pack(padx=10, pady=10)
    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    ttk.Button(top, text='OK', command=root.quit).pack(padx=10, pady=10)
    root.mainloop()

    base_date = cal.get_date()

    correct_wp_dates(base_date)
