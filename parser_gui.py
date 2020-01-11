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
from avito_parser import AvitoParser


class ParserGUI:
    def __init__(self):
        self.win = tk.Tk()
        self.win.resizable(0, 0)
        self.win.title("Avito parser")

        self.menu_bar = Menu(self.win)
        self.win.config(menu=self.menu_bar)

        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="New", command=self.new_process_win)
        self.options_menu.add_command(label="Open", command=self.open_process)
        self.options_menu.add_command(label="Save", command=self.save_process)

        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Update bot token", command=self.update_token)
        self.config_menu.add_command(label="Set path to Tesseract", command=self.set_path_tesseract)
        self.config_menu.add_command(label="Set path to Chrome driver", command=self.set_path_chrome)

        self.menu_bar.add_cascade(label="Process", menu=self.options_menu)
        self.menu_bar.add_cascade(label="Configure", menu=self.config_menu)

        self.log_window = tk.LabelFrame(self.win)
        self.log_window.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W)
        self.st = ScrolledText.ScrolledText(self.log_window, state='disabled', height=3)
        self.st.configure(width=40, height=20)
        self.st.pack(side=tk.TOP)
        self.text_handler = TextHandler(self.st)
        logging.basicConfig(filename='test.log', level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.text_handler)

        self.process_btn = tk.Button(self.win, text="Start", state="disabled", command=self.start_callback)
        self.process_btn.grid(column=0, row=1)

        self.city = ""
        self.quest = ""
        self.depth = "max"
        self.page_range = [0, 0]
        self.ads = []
        self.file_name = ""
        self.json_data = None

        self.win.mainloop()

    def new_process_win(self):
        process_win = tk.Tk()
        process_win.resizable(50, 50)
        process_win.lift(aboveThis=self.win)
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
                self.city = city_entered.get()
                self.quest = quest_entered.get()
                if not depth_entered.get():
                    messagebox.showwarning("Depth isn't specified, default equals to max possible value")
                    self.depth = "max"
                    self.save_process()
                else:
                    self.depth = depth_entered.get()
                    self.save_process()
                process_win.destroy()

        add_btn = tk.Button(process_win, text="Add", command=add_item)
        add_btn.grid(column=0, row=3)

    def save_process(self):
        file_name = "{0}_{1}_{2}_{3}_{4}_{5}".format(self.city, self.quest, self.depth,
                                                     str(self.page_range[0]), str(self.page_range[1]), date.today())
        process = {
            "city": self.city,
            "quest": self.quest,
            "page_parsed": self.page_range[0],
            "total_pages": self.page_range[1],
            "ads": self.ads
        }
        with open(r"processes/{0}.json".format(file_name), 'w', encoding='utf8') as out_file:
            json.dump(process, out_file, ensure_ascii=False)
        # out_file.close()
        print("saved!")
        return file_name

    def open_process(self):
        self.win.file_name = filedialog.askopenfilename(filetypes=(("JSON data", ".json"), ("all", "*.*")))
        with open(self.win.file_name, 'r+', encoding='utf8') as in_file:
            self.file_name = self.win.file_name
            self.json_data = json.load(in_file)
        self.process_btn.configure(state='active')
        logging.info("file {0} is loaded".format(self.win.file_name))
        print("opened!")

    def update_token(self):
        print("updated!")

    def set_path_tesseract(self):
        print("tesseract set!")

    def set_path_chrome(self):
        print("chrome set!")

    def start_callback(self):
        self.process_btn.configure(text="Stop", command=self.stop_callback)
        print("started!")
        # c = json_data["city"]
        # q = json_data["quest"]
        avito_parser = AvitoParser(2.5, "Moskva".lower(), "Диван")
        avito_parser.parse_urls()

    def stop_callback(self):
        # code
        self.process_btn.configure(text="Start", command=self.start_callback)
        print("stopped!")




