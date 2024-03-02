# Coverage: 92%
import unittest
from unittest import mock
from test.support import requires
import tkinter as tk
from idlelib import chatgpt
from idlelib import idleai



class TestChatGPT(unittest.TestCase):

    @classmethod
    def mock_askChatGPT(cls, prompt):
        cls.chatgpt.conversation._add_prompt_to_conversation(prompt)
        cls.chatgpt.conversation._add_response_to_conversation("MOCKED_RESPONSE")

    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.chatgpt = chatgpt.ChatGPT(cls.root, '{noto sans mono} 18 normal')
        cls.chatgpt.conversation.ask = cls.mock_askChatGPT

    @classmethod
    def tearDownClass(cls):
        cls.root.update_idletasks()
        cls.root.destroy()
        del cls.root, cls.chatgpt

    def test_init(self):
        self.assertEqual(self.chatgpt.title(), "ChatGPT")
        self.assertEqual(len(self.chatgpt.input_text.get("1.0", "end")), 1) # Check input field is empty on init
        self.assertEqual(self.chatgpt.input_label["text"], "Send a message to ChatGPT:") # Check input label is correct
        self.assertEqual(len(self.chatgpt.response_text.get("1.0", "end")), 1) # Check response field is empty on init
        self.assertEqual(self.chatgpt.generate_response_button["text"], "Generate Response") # Check button text is correct

    def test_generate_gpt_response(self):
        self.chatgpt.input_text.delete("1.0", "end")
        self.chatgpt.response_text.delete("1.0", "end")
        self.chatgpt.input_text.insert("end", "Hello")
        self.chatgpt.generate_gpt_response()
        self.assertNotEqual(len(self.chatgpt.response_text.get("1.0", "end")), 1) # Checks response not empty
        self.assertEqual(len(self.chatgpt.input_text.get("1.0", "end")), 1) # Checks input is empty after generate_gpt_response()
        self.assertIn("MOCKED_RESPONSE", self.chatgpt.response_text.get("1.0", "end")) # Checks mocked response is now in response field
        self.chatgpt.response_text.delete("1.0", "end")

    # Check empty input field inserts error into input field
    def test_empty_generate_gpt_response(self):
        self.chatgpt.input_text.delete("1.0", "end")
        self.chatgpt.response_text.delete("1.0", "end")
        self.chatgpt.generate_gpt_response()
        self.assertEqual(self.chatgpt.response_text.get("1.0", "end"), "\n"+"System: Please enter some text before generating response.\n\n")
        self.chatgpt.response_text.delete("1.0", "end")

if __name__ == "__main__":
    from unittest import main
    main('idlelib.idle_test.test_chatgpt', verbosity=2)