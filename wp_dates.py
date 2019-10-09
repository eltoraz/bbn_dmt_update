# wp_dates.py - skeleton for dmt manipulation code
import datetime
import tkinter
from tkinter import ttk

from tkcalendar import DateEntry

import csv_ops
import dmt
import log

baq = 'BBN_WP_Dates'                        # Epicor BAQ ID to export via DMT
scratch_dir = 'scratch\\'                   # folder to write temp CSV files
csv = scratch_dir + baq + '.csv'            # DMT-exported CSV file
new_csv = scratch_dir + 'Job_Assembly.csv'  # CSV to re-import into DMT
dmt_phase = 'Job Assembly'                  # DMT phase for the import step

new_csv2 = scratch_dir + 'Job_Head.csv'     # need to run DMT import twice,
dmt_phase2 = 'Job Header'                   #  unsetting the "new job" flag

# check that the scratch directory exists, and create it if not
csv_ops.check_scratch(scratch_dir)

# export the BAQ to a CSV file
dmt.dmt_export(baq, csv)

# read the data into this program
data = csv_ops.import_csv(csv)

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

# do stuff to the data
new_data = []
new_data2 = []
for row in data:
    # perform data transformations on each row from the exported dataset
    new_row = {}
    new_row['Company'] = row['Company']
    new_row['Plant'] = row['Site']
    new_row['JobNum'] = row['Job Number']
    new_row['AssemblySeq'] = row['Asm']
    new_row['PartNum'] = row['Part']
    new_row['DueDate'] = (base_date + datetime.timedelta(days=int(row['Lead']))).strftime('%m/%d/%y')
    new_data.append(new_row)
    
    new_row2 = {}
    new_row2['Company'] = row['Company']
    new_row2['Plant'] = row['Site']
    new_row2['JobNum'] = row['Job Number']
    new_row2['PartNum'] = row['Part']
    new_row2['NewlyAdded_c'] = False
    new_data2.append(new_row2)

# headers for the CSV file to import - make sure they match the mapping in the data manipulation above
headers = ['Company', 'Plant', 'JobNum', 'AssemblySeq', 'PartNum', 'DueDate']
headers2 = ['Company', 'Plant', 'JobNum', 'PartNum', 'NewlyAdded_c']

# export the changes to a CSV file formatted for the specified DMT phase
csv_ops.export_csv(headers, new_data, new_csv)
csv_ops.export_csv(headers2, new_data2, new_csv2)

# run DMT to import the changes into Epicor
dmt.dmt_import(dmt_phase, new_csv)
dmt.dmt_import(dmt_phase2, new_csv2)
