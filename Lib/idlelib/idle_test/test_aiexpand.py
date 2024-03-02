# Coverage: 98%
"Test aiexpand."

from idlelib.aiexpand import AIExpand
from idlelib.idleai import AICompletion
import unittest
from test.support import requires
import tkinter as tk
from tkinter import Text, Tk
# from unittest.mock import Mock
# import idlelib.aiexpand as ax


class DummyEditwin(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idleai = AICompletion()

class AIExpandTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()
        cls.editwin = DummyEditwin(cls.tk)
        cls.idle_ai = AICompletion()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()
        del cls.tk, cls.editwin, cls.idle_ai

    def setUp(self):
        self.editwin.delete('1.0', 'end')
        self.ai_expand = AIExpand(self.editwin, self.editwin.idleai, '{noto sans mono} 18 normal')

    def tearDown(self):
        self.editwin.delete('1.0', 'end')

    # Test that the listbox is created
    def test_create_listbox(self):
        self.ai_expand.create_listbox()
        self.assertTrue(self.ai_expand.listbox)
        self.assertTrue(self.ai_expand.listbox_win)
        self.assertEqual(self.ai_expand.initial_content, self.editwin.get("1.0", "end-1c"))

    # Test that the listbox is destroyed
    def test_revert(self):
        self.editwin.insert('insert', 'Initial Content')
        self.ai_expand.create_listbox()
        self.editwin.delete("1.0", "end")
        self.editwin.insert("insert", "New content")
        self.ai_expand.revert()
        self.assertEqual(self.editwin.get("1.0", "end-1c"), "Initial Content")
        self.assertIsNone(self.ai_expand.listbox)

    # Test that the preview is displayed and deleted after listbox is destroyed
    def test_display_preview(self):
        self.editwin.insert("end", "Initial content")
        self.ai_expand.create_listbox()
        self.ai_expand.listbox.insert("end", "Suggestion 1")
        self.ai_expand.listbox.insert("end", "Suggestion 2")
        self.ai_expand.listbox.selection_set(0)
        self.ai_expand.display_preview(None)
        self.assertEqual(self.editwin.get("1.0", "end-1c"), "Initial contentSuggestion 1")

    # Test that suggestion is inserted into the editwin
    def test_autofill_suggestion(self):
        self.editwin.insert("end", "Initial content")
        self.ai_expand.create_listbox()
        self.ai_expand.listbox.insert("end", "Suggestion 1")
        self.ai_expand.listbox.insert("end", "Suggestion 2")
        self.ai_expand.listbox.selection_set(1)
        self.ai_expand.autofill_suggestion()
        self.assertEqual(self.editwin.get("1.0", "end-1c"), "Initial contentSuggestion 2")
        self.assertIsNone(self.ai_expand.listbox_win)

    # Test expand word event opens listbox and inserts suggestions
    def test_expand_word_event(self):
        def mock_getline():
            return "word"

        def mock_getcontext():
            return "Some context"

        def mock_get_expansion_suggestions(line, context):
            return ["Suggestion 1", "Suggestion 2"]

        self.ai_expand.getline = mock_getline
        self.ai_expand.getcontext = mock_getcontext
        self.ai_expand.get_expansion_suggestions = mock_get_expansion_suggestions

        event = object()
        result = self.ai_expand.expand_word_event(event)

        self.assertEqual(result, "break")
        self.assertEqual(self.ai_expand.suggestions, ["Suggestion 1", "Suggestion 2"])
        self.assertEqual(self.ai_expand.listbox.get(0), "Suggestion 1")
        self.assertEqual(self.ai_expand.listbox.get(1), "Suggestion 2")     

    # Test line of current cursor position is returned
    def test_getline(self):
        self.editwin.insert("end", "Line 1\nLine 2\nLine 3")
        self.editwin.mark_set("insert", "2.3")  # Set the cursor to the second line
        line = self.ai_expand.getline()
        self.assertEqual(line, "Line 2")

    # Test context of above the line of the current cursor position is returned
    def test_getcontext(self):
        self.editwin.insert("end", "Line 1\nLine 2\nLine 3")
        self.editwin.mark_set("insert", "2.3")  
        context = self.ai_expand.getcontext().strip()
        self.assertEqual(context, "Line 1")
        
    # Test expansion suggestions are correctly returned from idleai.AICompletion.complete
    def test_get_expansion_suggestions(self):
        line = "word"
        context = "This is some context"
        suggestions = self.ai_expand.get_expansion_suggestions(line, context)
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        unique_suggestions = set(suggestions)
        self.assertEqual(len(suggestions), len(unique_suggestions))

if __name__ == '__main__':
    unittest.main(verbosity=2)

