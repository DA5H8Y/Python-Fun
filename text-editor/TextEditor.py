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
    window.title(f"Simple Text Editor - {filepath}")

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
    window.title(f"Simple Text Editor = {filepath}")
        
###main program
window = Tk()
window.title("Simple Text Editor")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1) #Only the second column will grow

txt_edit = Text(window)
frm_btns = Frame(window, relief=RAISED, border=2)
btn_open = Button(frm_btns, text="Open", command=open_file)
btn_save = Button(frm_btns, text="Save As...", command=saveas_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_btns.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
