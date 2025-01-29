import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

client = InferenceClient(
	provider="together",
	api_key=os.getenv("HF_ACCESS_TOKEN")
)

def formatQuery(instructions, query):
    return f"Follow the instructions to answer the user query\ninstructions:{instructions}\nquery:{query}"

systemInstructions = ("you are a cowboy, always start your responses with howdy partna'"
                      "you can make calls to an API endpoint at localhost:9000/orders/<clientId>"
                      "for example: to get information about past orders made by client 88, call the method curl -post 'localhost:9000/orders/88'")
userQuery = "how do you recommend I can find out more about the orders made by client with id 9?"

messages = [
	{
		"role": "user",
		"content": formatQuery(systemInstructions, userQuery)
	}
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1", 
	messages=messages, 
	max_tokens=500
)

print(completion.choices[0].message)