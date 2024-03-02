# Coverage: 97%
import unittest
from unittest import mock
from test.support import requires
from tkinter import Tk
from idlelib import idleaiconfig as iac

# based off the gui tests from test_query.py

class TestAiConfig(unittest.TestCase):
    @classmethod
    def mock_set_api_key(cls, key):
        cls.api_key = key

    @classmethod
    def mock_get_api_key(cls):
        return cls.api_key

    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = root = Tk()
        cls.root.withdraw()
        cls.ai_config = iac.IdleAIConfig(root, '{noto sans mono} 18 normal', _utest=True)
        cls.ai_config.set_api_key = cls.mock_set_api_key
        cls.ai_config.get_api_key = cls.mock_get_api_key
        cls.ai_config.destroy = mock.Mock()
        cls.api_key = "" # default api key for mocking

    @classmethod
    def tearDownClass(cls):
        del cls.ai_config.destroy
        del cls.ai_config
        cls.root.destroy()
        del cls.root
    
    # Make sure everything in the window starts in the correct state
    def test_init(self):
        self.assertEqual(self.ai_config.title(), "Idle AI Config")
        self.assertEqual(self.ai_config.curr_key_label["text"], "Current OpenAI Key:")
        self.assertEqual(self.ai_config.curr_key_text["show"], "*") # make sure the current key is hidden
        self.assertEqual(self.ai_config.curr_key_text["text"], "") # make sure current get is set to mock start value
        self.assertEqual(self.ai_config.curr_key_text["disabledbackground"], "white") # make sure styling on the current key is correct
        self.assertEqual(self.ai_config.curr_key_text["disabledforeground"], "black")
        self.assertEqual(self.ai_config.new_key_label["text"], "New OpenAI API Key:")
        self.assertEqual(self.ai_config.key_entry["show"], "*") # make sure the new key is hidden
        self.assertEqual(self.ai_config.show_button["text"], "Show Current Key")
        self.assertEqual(self.ai_config.should_show, True) # make sure the show button is in the correct state
        self.assertEqual(self.ai_config.update_button["text"], "Update API Key")
        self.assertEqual(self.ai_config.exit_button["text"], "Exit")

    # make sure hitting the show button toggles whether or not the key is visible
    def test_toggle_show_key(self):
        self.assertEqual(self.ai_config.curr_key_text["show"], "*")
        self.ai_config.show_button.invoke()
        self.assertEqual(self.ai_config.curr_key_text["show"], "")
        self.ai_config.show_button.invoke()
        self.assertEqual(self.ai_config.curr_key_text["show"], "*")

    # make sure that clicking the update button updates the key inside of the current key entry
    def test_update_key(self):
        self.assertEqual(self.ai_config.key_entry["text"], "")
        self.ai_config.key_entry.insert(0, "test")
        self.ai_config.update_button.invoke()
        self.assertEqual(TestAiConfig.api_key, "test")