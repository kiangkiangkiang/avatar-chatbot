from typing import Callable

from openai import OpenAI

from chatbot.session import sessions
from chatbot.utils.logger import logger


class OpenAITools:
    def __init__(self):
        self.client = OpenAI()

    @property
    def dummy_response(self):
        return {
            "text": "Default Response!",
            "facialExpression": "smile",
            "animation": "Rumba",
        }

    def create_chat_completions(
        self,
        messages,
        model="gpt-4o-mini",
        **kwargs,
    ):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
        )

        return completion.choices[0].message.content

    def create_chat_completions_with_func_try(
        self, unstable_func: Callable, user_id: str, max_try: int = 3, **kwargs
    ):
        current_retry_times = 0
        reponse = None
        while current_retry_times < max_try:
            try:
                reponse = self.create_chat_completions(**kwargs)
                result = unstable_func(reponse)
                sessions[user_id].append_memory(role="assistant", content=reponse)
                return result
            except Exception as e:
                logger.warning(
                    f"Fail to parse openai result: {e}\nRetry Times: {current_retry_times}\nResponse: {reponse}"
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
