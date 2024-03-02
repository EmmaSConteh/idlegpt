import tkinter as tk
import numpy as np
import soundcard as sc
from scipy.io.wavfile import write
import threading
import time
from idlelib import idleai

"""
This class defines the window that lets the user record audio for comment dictation
"""
class CommentDictation(tk.Toplevel):
    """
        parent = parent window
        fp = file pointer to temp file for audio saving
    """
    def __init__(self, parent, fp, font, _utest=False):
        tk.Toplevel.__init__(self, parent)
        self.fp = fp 
        self.font = font
        width = parent.winfo_width()
        height = parent.winfo_height()
        self.width = width // 2
        self.height = height // 2

        if not _utest:
            self.withdraw()

        self._setup_window()

        if not _utest:
            self.grab_set()
            self.wm_deiconify()
            self.wait_window()



    def _setup_window(self):
        self.title("Comment Dictation")
        self.geometry(f"{self.width}x{self.height}")
        self.text = tk.Label(self, text="Not Recording", font=self.font)
        self.text.pack()
        self.text2 = tk.Label(self, text="Press enter to start recording.", font=self.font)
        self.text2.pack()

        self.recording = False

        self.bind("<Return>", lambda _: self._set_recording(not self.recording))
    
    def _set_recording(self, status):
        if status:
            self.text.config(text="Recording...")
            self.text2.config(text="Press enter to stop.")
            self.recording = True
            t = threading.Thread(target=self._record_loop)
            t.start()
        else:
            # Extremley janky hack to get around weird behavior where the recording doesn't contain
            # the last second or so of audio... So we just keep recording for another 2 seconds...
            self.text.config(text="Stopping Recording...")
            self.text2.config(text="Please wait a moment...")
            self.update()
            self._record_wait()

            self.text.config(text="Not Recording.")
            self.text2.config(text="Please wait a moment...")
            self.update()
            self.recording = False
        self.update()

    # Pull this out in a function so it can be mocked in unit tests
    # Waits 2 extra seconds to make sure no audio gets chopped off in recording
    def _record_wait(self):
        time.sleep(2)
    
    def _record_loop(self):
        default_mic = sc.default_microphone()
        final_data = np.array([])

        with default_mic.recorder(samplerate=48000) as mic:
            while self.recording:
                new_data = mic.record(numframes=1024)
                final_data = np.concatenate((final_data, new_data), axis=None)
        
        write(self.fp, 48000, final_data)
        
        self.destroy()
