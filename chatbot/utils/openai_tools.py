from typing import Callable

from openai import OpenAI

from chatbot.utils.logger import logger


class OpenAITools:
    def __init__(self):
        self.client = OpenAI()

    def create_chat_completions(
        self,
        user_msg,
        model="gpt-4o-mini",
        system_prompt="You are a helpful assistant.",
        **kwargs,
    ):
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_msg,
                },
            ],
            **kwargs,
        )
        return completion.choices[0].message.content

    def create_chat_completions_with_func_try(
        self, unstable_func: Callable, max_try: int = 3, **kwargs
    ):
        current_retry_times = 0
        while current_retry_times < max_try:
            try:
                result = unstable_func(self.create_chat_completions(**kwargs))
                return result
            except Exception as e:
                logger.warning(
                    f"Fail to parse openai result: {e}\n Retry Times: {current_retry_times}"
                )
            finally:
                current_retry_times += 1
        raise ValueError(f"Cannot use {unstable_func} to parse the result of openai.")

    def text_to_speech(self, input_text: str):
        audio_response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=input_text,
        )
        return audio_response


openai_tools = OpenAITools()
