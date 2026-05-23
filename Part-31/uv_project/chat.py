import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

question = input("Ask ChatGPT anything: ")

print("\nSending message to OpenAI...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": question}
    ]
)

print("\nChatGPT says:")
print(response.choices[0].message.content)
