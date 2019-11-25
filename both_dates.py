import datetime
import tkinter
from tkinter import ttk

from tkcalendar import DateEntry

import po_dates
import wp_dates

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

po_dates.correct_po_dates(base_date)
wp_dates.correct_wp_dates(base_date)
