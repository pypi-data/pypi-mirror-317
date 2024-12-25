import pdb
from client import OpenAIClient

"""
client = OpenAI(
    api_key='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',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message.content)
"""

client = OpenAIClient('config.yaml')
client.request([{'role': 'user'}])
