from tkinter import *
from tkinter.ttk import Treeview

data = [
    ["key1", "value1"],
    ["key2", "value2"],
    ["key3", "value3"],
    ["key4", "value3"],
]

window = Tk()
window.title("encgui")
window.geometry("300x400")

columns = ("key", "value")
tree = Treeview(columns=columns, show="headings")
tree.pack(fill = BOTH, expand=1)

tree.heading("key", text="Key", anchor=W)
tree.heading("value", text="Value", anchor=W)

tree.column("#1", stretch=NO, width=150)
tree.column("#2", stretch=NO, width=150)

for record in data:
    tree.insert("", END, values=record)

window.mainloop()