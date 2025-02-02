import os
import json
import re
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Initialize the InferenceClient
client = InferenceClient(
    provider="together",
    api_key=os.getenv("HF_ACCESS_TOKEN")
)

def format_query(instructions, query):
    """Formats the query input for the model."""
    return f"Follow the instructions\ninstructions:{instructions}\nquery:{query}"

# Define system instructions
system_instructions = """
- You are a smart assistant that suggests the best tools to find relevant information to answer a query from the user.
- Use the following JSON format to structure your answers:
{ "suggested_tools": [ { "tool_name": <tool_name>, "parameters": { <parameter_name>: <value> } }, ... ] }
- You have access to the following tools:

1) ORDER API ENDPOINTS:
- GET /data/customer/{customer_id} - Retrieves all records for a specific customer ID.
- GET /data/product-category/{category} - Retrieves all records for a specific product category.
- GET /data/order-priority/{priority} - Retrieves all orders with a specific priority level.
- GET /data/total-sales-by-category - Retrieves total sales grouped by product category.
- GET /data/high-profit-products - Retrieves products above a specified profit threshold.

2) PRODUCT DATABASE DOCUMENT RETRIEVAL FUNCTION:
- retrieveDocuments(query, k) - Retrieves the top k documents most relevant to the query from the database.

*IMPORTANT: You must not execute the tools, only suggest their usage*
*IMPORTANT: Always use the argument values, never use placeholders. Plug in the parameters in your response*
*IMPORTANT: Once you know which tools to use, stop thinking and give your response*
"""

# User query
user_query = "I want to know more about orders made by customer 22 and I need to find out more information about the Ibanez acoustic guitars sold at the store, find out the most relevant document about this guitar."

# Prepare messages
messages = [{"role": "user", "content": format_query(system_instructions, user_query)}]

# Call the AI model
completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=messages,
    max_tokens=500
)

# Extract response content
response_text = completion.choices[0].message["content"]
print("Raw Response:\n", response_text)

# Step 1: Find the position of `</think>` and extract text after it
think_end_match = re.search(r'</think>\s*', response_text)

if think_end_match:
    json_start_index = think_end_match.end()
    json_text = response_text[json_start_index:].strip()

    # Step 2: Extract JSON using regex
    json_pattern = re.search(r'(\{.*\})', json_text, re.DOTALL)

    if json_pattern:
        json_content = json_pattern.group(1)  # Extract JSON
        try:
            parsed_response = json.loads(json_content)  # Parse JSON

            # Ensure it contains the expected structure
            if "suggested_tools" not in parsed_response:
                raise ValueError("Invalid JSON format: Missing 'suggested_tools' key")

            suggested_tools = parsed_response["suggested_tools"]

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
            suggested_tools = []
    else:
        print("Error: No JSON found after `</think>`.")
        suggested_tools = []
else:
    print("Error: `</think>` tag not found in response.")
    suggested_tools = []

# Define available tool functions
def get_customer_data(customer_id):
    print(f"Fetching order data for customer {customer_id}...")
    # Simulate API call
    return {"customer_id": customer_id, "orders": [{"order_id": 101, "status": "Completed"}]}

def retrieve_documents(query, k):
    print(f"Retrieving {k} most relevant documents for query: '{query}'...")
    # Simulate document retrieval
    return [{"title": "Ibanez Acoustic Guitar Specs", "content": "This guitar features..."}]

# Function mapping
tool_mapping = {
    "GET /data/customer/{customer_id}": lambda params: get_customer_data(params["customer_id"]),
    "retrieveDocuments": lambda params: retrieve_documents(params["query"], params["k"]),
}

# Execute suggested tools
results = {}
for tool in suggested_tools:
    tool_name = tool.get("tool_name")
    parameters = tool.get("parameters", {})

    if tool_name in tool_mapping:
        try:
            results[tool_name] = tool_mapping[tool_name](parameters)
        except Exception as e:
            print(f"Error executing tool {tool_name}: {str(e)}")
    else:
        print(f"Unknown tool: {tool_name}")

# Display the results
print("\nExecution Results:")
for tool, result in results.items():
    print(f"\nTool: {tool}\nResult: {result}")
