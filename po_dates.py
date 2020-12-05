# po_dates.py - update dates for POs
import datetime
import tkinter
from tkinter import ttk

from tkcalendar import DateEntry

import csv_ops
import dmt
import log

def correct_po_dates(base_date):
    baq = 'BBN_PO_Dates'                        # Epicor BAQ ID to export via DMT
    scratch_dir = 'scratch\\'                   # folder to write temp CSV files
    csv = scratch_dir + baq + '.csv'            # DMT-exported CSV file

    header_csv_unapprove = scratch_dir + 'PO_Hdr_Pre.csv'   # CSV to unapprove the PO to allow changes
    dtl_csv = scratch_dir + 'PO_Detail.csv'     # CSV to re-import into DMT
    rel_csv = scratch_dir + 'PO_Release.csv'    # CSV to change PO Release dates
    header_csv_reapprove = scratch_dir + 'PO_Hdr_Post.csv'  # CSV to re-approve the PO

    dmt_phase_hdr = 'Purchase Order Header'     # secondary DMT phase
    dmt_phase_rel = 'Purchase Order Release'
    dmt_phase_dtl = 'Purchase Order Detail'         # DMT phase for the import step

    # check that the scratch directory exists, and create it if not
    csv_ops.check_scratch(scratch_dir)

    # export the BAQ to a CSV file
    dmt.dmt_export(baq, csv)

    # read the data into this program
    data = csv_ops.import_csv(csv)
    log.log('po baq size:' + str(len(data)))

    # do stuff to the data
    pos = set()
    hdr_pre = []
    dtl_data = []
    rel_data = []
    hdr_post = []
    for row in data:
        curr_po = int(row['PO'])
        if curr_po not in pos:
            pos.add(curr_po)
            pre_row = {'Company': row['Company'], 'PONum': curr_po, 'VendorVendorID': row['Supplier ID'], 'Approve': False}
            post_row = {'Company': row['Company'], 'PONum': curr_po, 'VendorVendorID': row['Supplier ID'], 'Approve': True}
            hdr_pre.append(pre_row)
            hdr_post.append(post_row)

        dtl_row = {}
        rel_row = {}

        dtl_row['Company'] = row['Company']
        dtl_row['PONum'] = curr_po
        dtl_row['POLine'] = int(row['Line'])
        dtl_row['DueDate'] = (base_date + datetime.timedelta(days=int(row['Lead']))).strftime('%m/%d/%y')

        dtl_data.append(dtl_row)

        rel_row['Company'] = row['Company']
        rel_row['PONum'] = curr_po
        rel_row['POLine'] = dtl_row['POLine']
        rel_row['PORelNum'] = int(row['Release'])
        rel_row['DueDate'] = dtl_row['DueDate']

        rel_data.append(rel_row)

    log.log('po pre size:' + str(len(hdr_pre)))
    log.log('po dtl size:' + str(len(dtl_data)))
    log.log('po rel size:' + str(len(rel_data)))
    log.log('po post size:' + str(len(hdr_post)))

    # headers for the CSV file to import - make sure they match the mapping in the data manipulation above
    hdr_headers = ['Company', 'PONum', 'VendorVendorID', 'Approve']
    headers = ['Company', 'PONum', 'POLine', 'DueDate']
    rel_headers = ['Company', 'PONum', 'POLine', 'PORelNum', 'DueDate']

    # export the changes to a CSV file formatted for the specified DMT phase
    csv_ops.export_csv(hdr_headers, hdr_pre, header_csv_unapprove)
    csv_ops.export_csv(headers, dtl_data, dtl_csv)
    csv_ops.export_csv(rel_headers, rel_data, rel_csv)
    csv_ops.export_csv(hdr_headers, hdr_post, header_csv_reapprove)

    # run DMT to import the changes into Epicor
    dmt.dmt_import(dmt_phase_hdr, header_csv_unapprove)
    dmt.dmt_import(dmt_phase_dtl, dtl_csv)
    dmt.dmt_import(dmt_phase_rel, rel_csv)
    dmt.dmt_import(dmt_phase_hdr, header_csv_reapprove)

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

    correct_po_dates(base_date)
