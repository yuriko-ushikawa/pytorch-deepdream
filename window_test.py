import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Deep Dream')
root.geometry('800x600+50+50')
root.resizable(False,False)

def button_clicked():
    print(text.get())


button = ttk.Button(root, text='Click Me', command=button_clicked)
button.pack()

text = tk.StringVar()

ttk.Label(text="okienko").pack()
textbox = ttk.Entry(root, textvariable=text)
textbox.pack()

root.mainloop()