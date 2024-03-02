# Coverage: 92%
import unittest
from unittest import mock
from idlelib import commentdictation as cd
from test.support import requires
from tkinter import Tk

"""
CommentDictation is hard to test because it resolves around recording audio, but we can mock
this out and just test that the recording window works as expected
"""
class TestCommentDictation(unittest.TestCase):
    @classmethod
    def mock_record(cls):
        cls.comment_dictation.destroy()

    @classmethod
    def mock_wait(cls):
        pass # do nothing because we don't really need to wait for recording to terminate

    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = root = Tk()
        cls.root.withdraw()
        cls.comment_dictation = cd.CommentDictation(root, None, '{noto sans mono} 18 normal', _utest=True)
        cls.comment_dictation._record_loop = cls.mock_record
        cls.comment_dictation._record_wait = cls.mock_wait
        cls.comment_dictation.destroy = mock.Mock()
    
    # Make sure the widget initializes with correct text in the labels
    # saying that recording is not started, and to press enter to start
    def test_init(self):
        self.assertEqual(self.comment_dictation.text.cget("text"), "Not Recording")
        self.assertEqual(self.comment_dictation.text2.cget("text"), "Press enter to start recording.")
    
    # Make sure the widget updates correctly when you start recording
    def test_start_record(self):
        self.comment_dictation._set_recording(True)
        self.assertEqual(self.comment_dictation.text.cget("text"), "Recording...")
        self.assertEqual(self.comment_dictation.text2.cget("text"), "Press enter to stop.")
        self.assertEqual(self.comment_dictation.recording, True)

    # Make sure the widget stops correctly
    def test_stop_record(self):
        self.comment_dictation._set_recording(True)
        self.assertEqual(self.comment_dictation.text.cget("text"), "Recording...")
        self.assertEqual(self.comment_dictation.text2.cget("text"), "Press enter to stop.")
        self.assertEqual(self.comment_dictation.recording, True)
        self.comment_dictation._set_recording(False)
        self.assertEqual(self.comment_dictation.text.cget("text"), "Not Recording.")
        self.assertEqual(self.comment_dictation.text2.cget("text"), "Please wait a moment...")
        self.assertEqual(self.comment_dictation.recording, False)