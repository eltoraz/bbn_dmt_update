# po_dates.py - update dates for POs
import datetime
import tkinter
from tkinter import ttk

from tkcalendar import DateEntry

import csv_ops
import dmt
import log

baq = 'BBN_PO_Dates'                        # Epicor BAQ ID to export via DMT
scratch_dir = 'scratch\\'                   # folder to write temp CSV files
csv = scratch_dir + baq + '.csv'            # DMT-exported CSV file
new_csv = scratch_dir + 'PO_Detail.csv'     # CSV to re-import into DMT
dmt_phase = 'Purchase Order Detail'         # DMT phase for the import step

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
for row in data:
    new_row = {}
    new_row['Company'] = row['Company']
    new_row['PONum'] = int(row['PO'])
    new_row['POLine'] = int(row['Line'])
    new_row['DueDate'] = (base_date + datetime.timedelta(days=int(row['Lead']))).strftime('%m/%d/%y')
    new_data.append(new_row)

# headers for the CSV file to import - make sure they match the mapping in the data manipulation above
headers = ['Company', 'PONum', 'POLine', 'DueDate']

# export the changes to a CSV file formatted for the specified DMT phase
csv_ops.export_csv(headers, new_data, new_csv)

# run DMT to import the changes into Epicor
dmt.dmt_import(dmt_phase, new_csv)
