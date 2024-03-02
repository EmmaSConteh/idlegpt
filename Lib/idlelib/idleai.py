import os
import openai
from idlelib import idleaiconfig as iac

"""
This file serves as a wrapper around the Open AI API. It is used to query Open API models
and provides a simple interface for IDLE to use so that others can develop without
needing to understand how the API works internally.
"""

class AI:
    def __init__(self):
        # Read from config file
        openai.api_key = iac.IdleAIConfig.get_api_key()

class AITranscription(AI):
    def __init__(self):
        super().__init__()
    
    def transcribe(self, file) -> str:
        return openai.Audio.transcribe("whisper-1", file)["text"]

# Functionality for simple text autocomplete
class AICompletion(AI):
    def __init__(self):
        super().__init__()

    def complete(self, context, user_prompt):
        prompt = (
            f"You are an AI giving code autocompletion hints inside of a Python IDE"
            f"You should ONLY respond with Python code snippets, and never include any non python code before the response."
            f"This is the context of the rest of the code that the user is writing: {context}." 
            f"This is the sentence that you must expand upon: {user_prompt}.Provide a suggestion to complete the sentence."
            f"It should not include the part of the sentence already provided and should be correctly indented to match the rest of the code and where the cursor is."
            f"Example: If the user has written 'def foo():' and the cursor is on the next line, your response could be '    pass'.\n\n###\n\n"
        )
        response = openai.Completion.create(
            engine='text-davinci-003',
            # model='file-MjxBmoUOBgnhKKlH8k4sjhsU',
            prompt=prompt,
            max_tokens=100,
            temperature=0.9,
            n=8,
            stop=[" END"]
            
        )
    
        suggestions = [choice['text'] for choice in response['choices']]
        unique_suggestions = list(set(suggestions))
        return unique_suggestions

#TODO: Fix this error
# Functionality for having a chat GPT conversation
class AIConversation(AI):
    def __init__(self, setup_prompt: str | None = None):
        super().__init__()
        self._setup_conversation(setup_prompt)

    """
    These allow you to iterate through this object in a for each loop
    e.g.

    for (prompt, response) in ai_conversation:
        print(prompt, response)
    """
    def __iter__(self):
        # Start at index 2 because index 0 is the setup prompt
        # index 1 is the first user prompt
        # index 2 is the first gpt response
        current = 2 
        while current < len(self._conversation):
            yield (self._conversation[current - 1]['content'], self._conversation[current]['content'])
            current += 2

    """
    Ask a question to the chat GPT model and return the response
    """
    def ask(self, prompt: str) -> str:
        # used for reference: https://medium.com/geekculture/a-simple-guide-to-chatgpt-api-with-python-c147985ae28
        self._add_prompt_to_conversation(prompt)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._conversation
        )

        response = completion.choices[0].message.content
        self._add_response_to_conversation(response)
        return response

    """
    Helper methods for managing the conversation
    """

    def _setup_conversation(self, setup_prompt: str | None) -> None:
        # This starts the conversation by making sure Chat GPT knows it is helping users of IDLE
        # This essentially provides the context in which Chat GPT answers all of the questions
        if not setup_prompt:
            setup_prompt = "You are a helpful assistant answering questions for users of IDLE."

        self._conversation = [
            {
                "role": "system",
                "content": setup_prompt
            }
        ]
    
    def _add_prompt_to_conversation(self, user_prompt: str) -> None:
        self._conversation.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )
    
    def _add_response_to_conversation(self, gpt_response: str) -> None:
        self._conversation.append(
            {
                "role": "assistant",
                "content": gpt_response 
            }
        )

# Small test 
if __name__ == "__main__":
    conversation = AIConversation()
    conversation.ask("How do I print something in Python?")
    conversation.ask("Thank you for the response!")

    for (prompt, response) in conversation:
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")