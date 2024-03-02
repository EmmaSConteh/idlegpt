# Coverage: 97%
import unittest
from unittest.mock import patch
from idlelib import idleai as ia 

"""
Tests for the idleai wrapper around the open API package
We only test the AICompletion and AIConversation because 
AITranscription isn't really testable at that level.
"""

class TestAiCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ai_completion = ia.AICompletion()

    @patch("openai.Completion.create")
    # test that we can get a response from the API
    def test_complete(self, mock):
        context = "context"
        user_prompt = "user prompt"

        mock_response = {
            "choices": [
                {"text": "sample suggestion"},
                {"text": "sample suggestion 2"},
                
            ]
        }
        mock.return_value = mock_response
        result = self.ai_completion.complete(context, user_prompt)
        # make sure that the order of suggestions is consistent, because the way we are filtering out unique
        # suggestions is by converting to a set and then back to a list, which can possibly change the order
        result.sort()
        self.assertEqual(result, ["sample suggestion", "sample suggestion 2"])

class TestAiConversation(unittest.TestCase):
    @classmethod
    def fake_ask(cls, prompt, response):
        cls.ai_conversation._add_prompt_to_conversation(prompt)
        cls.ai_conversation._add_response_to_conversation(response)

    @classmethod
    def setUpClass(cls):
        cls.ai_conversation = ia.AIConversation()

    def setUp(self):
        self.ai_conversation._setup_conversation("This is a test prompt")

    # make sure that we start off not having asked any questions
    def test_init(self):
        i = 0
        for (_prompt, _response) in self.ai_conversation:
            i += 1
        self.assertEqual(i, 0)

    # test normal flow of conversation, and making sure that we can iterate through it and display everything
    def test_conversation(self):
        conversation = [
            ("What is 2+2?", "4"),
            ("How do I center a div?", "This is impossible."),
            ("How do I print something in Python?", "print('Hello World!')")
        ]

        with patch("idlelib.idleai.AIConversation.ask", wraps=self.fake_ask) as mock_ask:
            for (prompt, response) in conversation:
                self.ai_conversation.ask(prompt, response)
                mock_ask.assert_called_with(prompt, response)

        num_prompts = 0
        for i, (prompt, response) in enumerate(self.ai_conversation):
            num_prompts += 1
            self.assertEqual(prompt, conversation[i][0])
            self.assertEqual(response, conversation[i][1])
        self.assertEqual(num_prompts, 3)
