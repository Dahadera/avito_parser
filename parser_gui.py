import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
from tkinter import messagebox
#from tkinter import ttk
from tkinter import Frame
from tkinter import Button
from datetime import date
import tkinter.scrolledtext as ScrolledText
from text_handler import TextHandler
import logging


def add_new_process():
    item_win = tk.Tk()
    item_win.resizable(20, 20)
    item_win.title("New item")

    city_container = tk.LabelFrame(item_win)
    city_container.grid(column=0, row=0)
    city_label = tk.Label(city_container, width=8, text="City: ")
    city_label.grid(column=0, row=0, sticky=tk.E)
    city = tk.StringVar()
    city_entered = tk.Entry(city_container, width=15, textvariable=city)
    city_entered.grid(column=2, row=0)
    city_entered.focus()

    quest_container = tk.LabelFrame(item_win)
    quest_container.grid(column=0, row=1)
    quest_label = tk.Label(quest_container, width=8, text="Quest: ")
    quest_label.grid(column=0, row=1, sticky=tk.E)
    quest = tk.StringVar()
    quest_entered = tk.Entry(quest_container, width=15, textvariable=quest)
    quest_entered.grid(column=2, row=1)

    depth_container = tk.LabelFrame(item_win)
    depth_container.grid(column=0, row=2)
    depth_label = tk.Label(depth_container, width=8, text="Max depth: ")
    depth_label.grid(column=0, row=2, sticky=tk.E)
    depth = tk.StringVar()
    depth_entered = tk.Entry(depth_container, width=15, textvariable=depth)
    depth_entered.grid(column=2, row=2)

    save_process(city, quest, depth, page_range=[0, 0])
    # city, quest, depth search
    print("click!")
    # item_win.destroy)


def save_process(city, quest, depth, page_range):
    file_name = "{0}_{1}_{2}_{3}_{4}_{5}".format(str(city), str(quest), str(depth),
                                                 str(page_range[0]), str(page_range[1]), date.today())
    file = open(file_name, "w")

    print("saved!")

def open_process():
    process_btn.configure(state="active")
    print("opened!")

def update_token():
    print("updated!")

def set_path_tesseract():
    print("tesseract set!")

def set_path_chrome():
    print("chrome set!")

def start_callback():
    # code
    process_btn.configure(text="Stop", command=stop_callback)
    print("started!")

def stop_callback():
    #code
    process_btn.configure(text="Start", command=start_callback)
    print("stopped!")

win = tk.Tk()
win.resizable(0, 0)
win.title("Avito parser")

menu_bar = Menu(win)
win.config(menu=menu_bar)

options_menu = Menu(menu_bar,  tearoff=0)
options_menu.add_command(label="New", command=add_new_process)
options_menu.add_command(label="Open", command=open_process)
options_menu.add_command(label="Save", command=save_process)

config_menu = Menu(menu_bar,  tearoff=0)
config_menu.add_command(label="Update bot token", command=update_token)
config_menu.add_command(label="Set path to Tesseract", command=set_path_tesseract)
config_menu.add_command(label="Set path to Chrome driver", command=set_path_chrome)

menu_bar.add_cascade(label="Process", menu=options_menu)
menu_bar.add_cascade(label="Configure", menu=config_menu)

log_window = tk.LabelFrame(win)
log_window.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W)
st = ScrolledText.ScrolledText(log_window, state='disabled', height=3)
st.configure(width=40, height=20)
st.pack(side=tk.TOP)
text_handler = TextHandler(st)
logging.basicConfig(filename='test.log', level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(text_handler)

process_btn = tk.Button(win, text="Start", state="disabled", command=start_callback)
process_btn.grid(column=0, row=1, columnspan=1, rowspan=1)


win.mainloop()
print(1)