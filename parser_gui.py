import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk
from tkinter import Frame
from tkinter import Button
import tkinter.scrolledtext as ScrolledText
from text_handler import TextHandler
import logging


def add_to_watchlist():
    print("click!")

def save_process():
    print("saved!")

def open_process():
    print("opened!")

win = tk.Tk()
win.resizable(0, 0)
win.title("Avito parser")

win.grid_rowconfigure((0, 3), weight=2)

watchlist_button = ttk.Button(win, text="Add to watchlist", width=20, command=add_to_watchlist)
save_process_button = ttk.Button(win, text="Save process", width=20, command=save_process)
open_process_button = ttk.Button(win, text="Open process", width=20, command=open_process)


watchlist_button.grid(column=2, row=0, sticky=tk.E)
save_process_button.grid(column=2, row=1, sticky=tk.E)
open_process_button.grid(column=2, row=2, sticky=tk.E)

log_window = ttk.LabelFrame(win)
log_window.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W)

st = ScrolledText.ScrolledText(log_window, state='disabled', height=3)
st.configure(width=30, height=10)
st.pack(side=tk.LEFT)
text_handler = TextHandler(st)
logging.basicConfig(filename='test.log', level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(text_handler)



# watchlist_button = tk.Button(win, text="OK", command=add_to_watchlist);
# watchlist_button.pack()

win.mainloop()
print(1)