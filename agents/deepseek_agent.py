import os
import requests
from dotenv import load_dotenv

load_dotenv()

def call_deepseek_agent(prompt):
    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "max_tokens": 4096,
        "stop": ["null"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": [
        {
            "type": "function",
            "function": {
                "description": "<string>",
                "name": "<string>",
                "parameters": {},
                "strict": False
            }
        }
    ]
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("choices")[0].get("message").get("content")
    else:
        return "Error retrieving response from DeepSeek."
