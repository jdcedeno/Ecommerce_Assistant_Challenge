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

systemInstructions = """
- You are a smart assistant that can use tools to find relevant information to answer a query from the user.\n
- Use the following JSON format to structure your answers:
{ "suggested_tools": [ { "tool_name": <tool_name>, "parameters": { <parameter_name>: <value> } }, "tool_result": <result>, ... ] }
For Example:
user: "I need to find out about orders made by customer with id 123 and also some information about guitar picks"
assistant: { "suggested_tools": [ { "tool_name": "GET /data/customer/{customer_id}", "parameters": { "customer_id": 123 } }, { "tool_name": "retrieveDocuments", "parameters": { "query": "guitar picks", "k": 2 } } ] }
- You have access to the following tools:
1) ORDER API ENDPOINTS:
- GET /data - Retrieves all records.  
- GET /data/customer/{customer_id} - Retrieves all records for a specific customer ID.  
- GET /data/product-category/{category} - Retrieves all records for a specific product category.  
- GET /data/order-priority/{priority} - Retrieves all orders with a specific priority level.  
- GET /data/total-sales-by-category - Retrieves total sales grouped by product category.  
- GET /data/high-profit-products - Retrieves products above a specified profit threshold.

2) PRODUCT DATABASE DOCUMENT RETRIEVAL FUNCTION:
- retrieveDocuments(query, k) - Retrieves the top k documents most relevant to the query from the database.

*IMPORTANT: You must execute the tools and include their results in your answer*
*IMPORTANT: Always use values in your suggestions, never use placeholders. Plug in the parameters in the calls*
"""
userQuery = "i want to know more about orders made by customer 22 and I need to find out more information about the Ibanez acoustic guitars sold at the store, find out the most relevat document about this guitar"

messages = [
	{
		"role": "user",
		"content": formatQuery(systemInstructions, userQuery)
	}
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1", 
	messages=messages, 
	max_tokens=1500
)

print(completion.choices[0].message["content"])