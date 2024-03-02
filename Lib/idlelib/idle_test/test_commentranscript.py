# Coverage: 11%
import unittest
from idlelib import commenttranscript as ct

LINE_LIMIT = 70

"""
Tests actually transcribing the comment that has been dictated

This is basically impossible to actually unit test. It involves
    - reading audio data from a file
    - sending said audio data to openai for analysis
    - receving the transcript, formatting it and outputting it to the window

The only part that seemed possible to actually unit test was the
formatting, so that is what this file does.
"""
class TestCommentTranscript(unittest.TestCase):
    """
    Ensure that
    1. no lines are longer than 80 characters
    2. The comment is surrounded by triple " so it is enclosed in a 
       multiline comment
    """
    def test_format_transcript(self):
        transcript = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " \
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." \
            "Risus nullam eget felis eget nunc lobortis mattis. Eu non diam phasellus" \
            "vestibulum lorem sed. Massa eget egestas purus viverra. Nibh tellus molestie" \
            "nunc non blandit. Odio eu feugiat pretium nibh ipsum consequat nisl. Augue interdum" \
            " velit euismod in pellentesque massa. Facilisis sed odio morbi quis commodo odio. " \
            "Nisl pretium fusce id velit ut tortor pretium. Et sollicitudin ac orci phasellus egestas" \
            " tellus. Proin sed libero enim sed. In dictum non consectetur a erat nam at lectus urna. "\
            "Orci a scelerisque purus semper eget duis."

        transcript = {"text": transcript}
        
        transcript = ct._format_transcript(transcript)

        lines = transcript.split("\n")
        # Make sure no lines longer than 80 characters
        for line in lines:
            self.assertLessEqual(len(line), LINE_LIMIT)

        # Make sure first and last line are """\n
        self.assertEqual(lines[0], "\"\"\"")
        self.assertEqual(lines[-2], "\"\"\"") # -2 because -1 is an empty string (the line after the """)