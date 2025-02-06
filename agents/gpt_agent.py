import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def call_gpt_agent(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"), 
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful professional financial analyst."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content
