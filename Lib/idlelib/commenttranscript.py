import openai
import textwrap
import threading
import os
from idlelib import idleai
from tkinter import Toplevel, Label

"""
This file uses CommentDictation to get the recorded audio, and then actually uses that recorded data
to generate a transcript.
"""

# Basic class to display a dialogue while waiting for transcription
class WaitingDialog(Toplevel):
    def __init__(self, parent, font):
        Toplevel.__init__(self, parent)
        self.font = font
        self.title("Contacting our AI overlords...")

        # Get correct relative size from parent
        width = parent.winfo_width()
        height = parent.winfo_height()
        self.width = width // 2
        self.height = height // 2

        self.geometry(f"{self.width}x{self.height}")
        label = Label(self, text="Please wait a moment", font=self.font)
        label.pack()
        self.resizable(False, False)
        self.transient(parent)

    def wait(self):
        self.wait_window(self)

# Formats the transcript before output
def _format_transcript(transcript):
    text = transcript["text"]
    text_shortened_lines = "\n".join(textwrap.wrap(text)) # make sure no lines longer than 80 characters
    multi_line_comment = "\"\"\"" # multi line comments in python are started/ended with """
    return multi_line_comment + "\n" + text_shortened_lines + "\n" + multi_line_comment + "\n"

"""
Function to handle entire recording and transcribing process

tk_parent: reference to TK editor window
fd: file descriptor of the temp file to read from
name: name of the temp file
buffer: file data already stored in format that openai wants
"""

def transcribe_comment(tk_parent, buffer, font):

    # now the file contains the audio information
    # so we need to transcribe it

    ai = idleai.AITranscription()
    wait_dialog = WaitingDialog(tk_parent.top, font)
    # this is a dictionary so that we can mutate it in the below thread
    # if it were just a string it wouldn't work because of python's scoping rules
    # and how stack/heap values are allocated
    transcript = {"text": ""}

    def query_openai():
        try:
            transcript["text"] = ai.transcribe(buffer)
        except openai.error.AuthenticationError as e:
            transcript["text"] = "An authentication error occurred while querying openai:\n" + e._message + "\n\nPlease check your API key and try again."
        except Exception as e:
            transcript["text"] = "An unknown error occurred while querying openai. Your api key may be incorrect, or openai's servers might be down, or possibly something else unexpected occurred. Please try again later"
        wait_dialog.destroy() # kill waiting dialogue in original thread when done so execution continues

    t = threading.Thread(target=lambda: query_openai())
    t.start()

    wait_dialog.wait()

    transcript = _format_transcript(transcript)

    tk_parent.text.insert("insert", transcript)
