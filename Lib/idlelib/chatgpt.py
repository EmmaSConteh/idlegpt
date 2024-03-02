'''Provide ChatGPT window under 
'''

from idlelib.idleai import AIConversation
from tkinter import (Toplevel, Button, Label, Frame, scrolledtext, LEFT, RIGHT, font as tkfont)

from idlelib.config import idleConf

class ChatGPT(Toplevel):
    def __init__(self, parent, font):
        Toplevel.__init__(self, parent)

        self.conversation = AIConversation()

        # Set up window title
        self.parent = parent
        self.title("ChatGPT")

        # Set font from argument
        tk_font = font

        # Create scrollable response text box
        self.response_text = scrolledtext.ScrolledText(self, width=80, height=15, font=tk_font)
        self.response_text.pack()

        # Create input label
        self.input_label = Label(self, text="Send a message to ChatGPT:", font=tk_font)
        self.input_label.pack()

        # Create scrollable input text box
        self.input_text = scrolledtext.ScrolledText(self, width = 80, height=3, font=tk_font)
        self.input_text.pack()

        # Create button to generate response (runs generate_gpt_response function)
        self.generate_response_button_frame = Frame(self)
        self.generate_response_button = Button(self.generate_response_button_frame, text="Generate Response", command=self.generate_gpt_response, font=tk_font)
        self.generate_response_button.pack()
        self.generate_response_button_frame.pack()

        # Bind to run on_resize
        self.bind('<Configure>', self.on_resize)

    # Update width if window is resized
    def on_resize(self, event):
        self.response_text.configure(width=event.width)
        self.input_text.configure(width=event.width)

    def generate_gpt_response(self) -> None:
        if(len(self.input_text.get("1.0", "end")) == 1): # Checking if input box is empty
            self.response_text.insert("end","\n"+"System: Please enter some text before generating response.\n")
            return
        
        # Handles clearing text from input box and moving it into conversation history
        gpt_prompt = self.input_text.get("1.0", "end")
        self.input_text.delete("1.0", "end")
        self.response_text.insert("end","\n"+"User: "+gpt_prompt)
        self.conversation.ask(gpt_prompt)
        self.response_text.insert("end", "\n"+"ChatGPT: "+self.conversation._conversation[-1]['content']+"\n")