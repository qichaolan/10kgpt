import openai
from time import sleep

class ChatGPT:
    def __init__(self, api_key):
        openai.api_key = api_key

    def summarize_financial_statements(self, tokens: str):
        prompt = f"Summarize this for a stock buyer:\n{tokens}"

        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )

        # sleep 1 sec to match the requirement 
        # that the ChatGPT API has a limit on the number of queries per minute.
        sleep(1)

        return response["choices"][0]["text"]

    def finalize_statements(self, tokens: str):
        prompt = f"Correct this to standard English::\n{tokens}"

        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )

        # sleep 1 sec to match the requirement 
        # that the ChatGPT API has a limit on the number of queries per minute.
        sleep(1)

        return response["choices"][0]["text"]