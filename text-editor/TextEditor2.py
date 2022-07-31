from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing"""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    txt_edit.delete("1.0", END) #Delete content of textbox
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read() #Read file content
        txt_edit.insert(END, text) #Insert file content into textbox
    root.title(f"Simple Text Editor v2.0 - {filepath}")

def saveas_file():
    """Save the current file as a new file"""
    filepath = asksaveasfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not filepath:
        return

    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", END)
        output_file.write(text)
    root.title(f"Simple Text Editor v2.0 = {filepath}")

def wrap_text(value):
    global bool_wrapText
    if value:
        txt_edit['wrap'] = 'word'
    else:
        txt_edit['wrap'] = 'none'
    bool_wrapText = value
        
###main program - replaces buttons with menu
root = Tk()
root.title("Simple Text Editor v2.0")
root.option_add('*tearOff', FALSE) #Switch menu tearOff option off

root.rowconfigure(0, minsize=800, weight=1)
root.columnconfigure(0, minsize=800, weight=1)
root.columnconfigure(1, minsize=10, weight=0)
root.rowconfigure(1, minsize=10, weight=0)

txt_edit = Text(root)
txt_edit.grid(row=0, column=0, sticky="nsew")
s_editV = Scrollbar(root, orient=VERTICAL, command=txt_edit.yview) #Add a vertical scrollbar
s_editV.grid(column=1, row=0, sticky='ns')
txt_edit['yscrollcommand'] = s_editV.set
s_editH = Scrollbar(root, orient=HORIZONTAL, command=txt_edit.xview) #Add a horizontal scrollbar
s_editH.grid(column=0, row=1, sticky='ew')
txt_edit['xscrollcommand'] = s_editH.set

###New Statusbar
lbl_status = Label(text="Staus: ", relief='sunken', font="TkTooltipFont", justify='left')
lbl_status.grid(column=0, row=2, columnspan=2, sticky='ew')

###New menu section
menubar = Menu(root)
menu_file = Menu(menubar)
menu_view = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_view, label='View')

bool_wrapText = BooleanVar()
bool_wrapText.set(True)

menu_file.add_command(label='Open...', underline=0, command=open_file, accelerator='Ctrl+O')
menu_file.add_command(label='Save As...', command=saveas_file)

menu_view.add_checkbutton(label='Wrap Text', onvalue=1, offvalue=0, variable=bool_wrapText, command=lambda :wrap_text(not(bool_wrapText)))

root['menu'] = menubar
root.mainloop()
