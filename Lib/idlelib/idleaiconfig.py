from tkinter import (Toplevel, Button, Label, Entry, Frame)
import tkinter as tk
from idlelib import config 
import configparser

class IdleAIConfig(Toplevel):
    CFG_PATH = f"{config.idleConf.GetUserCfgDir()}/ai.conf" # path to ai key file

    def __init__(self, parent, font, _utest=False):
        Toplevel.__init__(self, parent)

        if not _utest:
            self.withdraw()

        self.parent = parent
        self.title("Idle AI Config")

        self.curr_key_label = Label(self, text="Current OpenAI Key:", font=font)
        self.curr_key_label.pack()

        self.curr_key_text = Entry(self, width=50, font=font)
        self.curr_key_text.config(show="*")
        self.curr_key_text.configure(disabledbackground="white", disabledforeground="black")
        self.update_curr_key_display()
        self.curr_key_text.pack()

        self.new_key_label = Label(self, text="New OpenAI API Key:", font=font)
        self.new_key_label.pack()

        self.key_entry = Entry(self, width=50, font=font)
        self.key_entry.config(show="*")
        self.key_entry.pack()

        self.button_frame = Frame(self)

        self.show_button = Button(self.button_frame, text="Show Current Key", font=font, command=self.toggle_show_key)
        self.should_show = True
        self.show_button.pack(side=tk.LEFT)

        self.update_button = Button(self.button_frame, text="Update API Key", font=font, command=self.update_api_key)
        self.update_button.pack(side=tk.LEFT)

        self.exit_button = Button(self.button_frame, text="Exit", font=font, command=self.destroy)
        self.exit_button.pack(side=tk.LEFT)

        self.button_frame.pack()

        if not _utest:
            self.grab_set()
            self.wm_deiconify()
            self.wait_window()
    
    @staticmethod
    def get_api_key() -> str:
        parser = configparser.ConfigParser()
        parser.read(IdleAIConfig.CFG_PATH)
        try:
            return parser["mandatory"]["api_key"]
        except KeyError: 
            # occurs when the file is empty / doesn't exist / doesn't have the api_key field
            return ""

    @staticmethod
    def set_api_key(key: str) -> None:
        parser = configparser.ConfigParser()
        parser["mandatory"] = {"api_key": key}
        with open(IdleAIConfig.CFG_PATH, 'w') as configfile:
            parser.write(configfile)
        
    def toggle_show_key(self) -> None:
        if self.should_show:
            self.show_button.config(text="Hide Current Key")
            self.curr_key_text.config(show="")
        else:
            self.curr_key_text.config(show="*")
            self.show_button.config(text="Show Current Key")
        self.should_show = not self.should_show

    # update the text showing the current api key
    def update_curr_key_display(self) -> None:
        text = self.curr_key_text

        text.config(state="normal")  # Enable editing
        text.delete("0", "end")  # Clear existing text

        curr_key = self.get_api_key()

        text.insert("0", curr_key)  # Insert new text
        text.config(state="disabled")  # Disable editing

    # update the actual key saved in file and the display
    def update_api_key(self) -> None:
        # update actual file
        new_key = self.key_entry.get()
        self.set_api_key(new_key)

        self.update_curr_key_display()