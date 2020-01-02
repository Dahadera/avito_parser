import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk
from tkinter import Frame
from tkinter import Button
import json
from datetime import date
import tkinter.scrolledtext as ScrolledText
from text_handler import TextHandler
import logging
from avito_parser import avitoParser


def new_process_win():
    process_win = tk.Tk()
    process_win.resizable(50, 50)
    process_win.lift(aboveThis=win)
    process_win.title("New process")

    city_container = tk.LabelFrame(process_win)
    city_container.grid(column=0, row=0)
    city_label = tk.Label(city_container, width=8, text="City: ")
    city_label.grid(column=0, row=0, sticky=tk.E)
    city = tk.StringVar()
    city_entered = ttk.Entry(city_container, width=15, textvariable=city)
    city_entered.grid(column=2, row=0)
    city_entered.focus()

    quest_container = tk.LabelFrame(process_win)
    quest_container.grid(column=0, row=1)
    quest_label = tk.Label(quest_container, width=8, text="Quest: ")
    quest_label.grid(column=0, row=1, sticky=tk.E)
    quest = tk.StringVar()
    quest_entered = ttk.Entry(quest_container, width=15, textvariable=quest)
    quest_entered.grid(column=2, row=1)

    depth_container = tk.LabelFrame(process_win)
    depth_container.grid(column=0, row=2)
    depth_label = tk.Label(depth_container, width=8, text="Max depth: ")
    depth_label.grid(column=0, row=2, sticky=tk.E)
    depth = tk.StringVar()
    depth_entered = ttk.Entry(depth_container, width=15, textvariable=depth)
    depth_entered.grid(column=2, row=2)

    def add_item():
        if not city_entered.get():
            messagebox.showerror("City isn't specified!")
        elif not quest_entered.get():
            messagebox.showerror("Quest is empty!")
        else:
            if not depth_entered.get():
                messagebox.showwarning("Depth isn't specified, default equals to max possible value")
            save_process(city_entered.get(), quest_entered.get(), depth_entered.get(), page_range=[0, 0], ads=[])
            process_win.destroy()

    add_btn = tk.Button(process_win, text="Add", command=add_item)
    add_btn.grid(column=0, row=3)


def save_process(city, quest, depth, page_range, ads):
    file_name = "{0}_{1}_{2}_{3}_{4}_{5}".format(city, quest, depth,
                                                 str(page_range[0]), str(page_range[1]), date.today())
    process = {
        "city": city,
        "quest": quest,
        "page_parsed": page_range[0],
        "total_pages": page_range[1],
        "ads": ads
    }
    with open(r"processes/{0}.json".format(file_name), 'w', encoding='utf8') as out_file:
        json.dump(process, out_file, ensure_ascii=False)
    # out_file.close()
    print("saved!")
    return file_name


def open_process():
    win.file_name = filedialog.askopenfilename(filetypes=(("JSON data", ".json"), ("all", "*.*")))
    with open(win.file_name, 'r+', encoding='utf8') as in_file:
        json_data = json.load(in_file)
    logging.info("file {0} is loaded".format(win.file_name))
    print("opened!")


def update_token():
    print("updated!")

def set_path_tesseract():
    print("tesseract set!")

def set_path_chrome():
    print("chrome set!")


def start_callback():
    process_btn.configure(text="Stop", command=stop_callback)
    print("started!")
    avito_parser = avitoParser(2.5, json_data["city"], json_data["quest"])
    avito_parser.gen_urls()


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
options_menu.add_command(label="New", command=new_process_win)
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
process_btn.grid(column=0, row=1)

json_data = None

win.mainloop()
