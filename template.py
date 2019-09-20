# template.py - skeleton for dmt manipulation code
import datetime
import tkinter
from tkinter import ttk

from tkcalendar import DateEntry

import csv_ops
import dmt
import log

baq = '[BAQ NAME]'                          # Epicor BAQ ID to export via DMT
scratch_dir = 'scratch\\'                   # folder to write temp CSV files
csv = scratch_dir + baq + '.csv'            # DMT-exported CSV file
new_csv = scratch_dir + '[DMT_IMPORT].csv'  # CSV to re-import into DMT
dmt_phase = '[FULL DMT PHASE NAME]'         # DMT phase for the import step

# check that the scratch directory exists, and create it if not
csv_ops.check_scratch(scratch_dir)

# export the BAQ to a CSV file
dmt.dmt_export(baq, csv)

# read the data into this program
data = csv_ops.import_csv(csv)

# vvvvvvvvv DELETE IF YOU DON'T NEED A DATE PICKER IN THIS OPERATION vvvvvvvvvvvvvvvvvvvvvv
# also delete the import statements on lines 2-6
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
# ^^^^^^^^^ DELETE IF YOU DON'T NEED A DATE PICKER IN THIS OPERATION ^^^^^^^^^^^^^^^^^^^^^^

# do stuff to the data
new_data = []
for row in data:
    # perform data transformations on each row from the exported dataset
    pass        # delete this line when doing the actual data manipulations

# headers for the CSV file to import - make sure they match the mapping in the data manipulation above
headers = []        # check the DMT template builder for the field names you need!

# export the changes to a CSV file formatted for the specified DMT phase
csv_ops.export_csv(headers, new_data, new_csv)

# run DMT to import the changes into Epicor
dmt.dmt_import(dmt_phase, new_csv)
