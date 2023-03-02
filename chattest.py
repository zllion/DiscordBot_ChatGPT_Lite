import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
chat = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant. Make the answer precise"},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"},
        {"role": "assistant", "content":"The 2020 World Series was played at Globe Life Field in Arlington, Texas."},
        {"role": "user", "content": "Where was the previous one?"}
    ]
)

print(chat["choices"][0]['message']["content"])
print("token used", chat["usage"]["total_tokens"])