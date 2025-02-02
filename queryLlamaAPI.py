import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

client = InferenceClient(
	provider="hf-inference",
	api_key=os.getenv("HF_ACCESS_TOKEN")
)

messages = [
	{
		"role": "user",
		"content": "if I give you a system prompt explaining how to use tools: an API endpoint usage description and a function with instructions on how to call it and what information these endpoints and functions return. Can you suggest which tools to use and how to use them given a user prompt? You can assume the user will ask questions that can be answered by using the given tools."
	}
]

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct", 
	messages=messages, 
	max_tokens=500
)

print(completion.choices[0].message)