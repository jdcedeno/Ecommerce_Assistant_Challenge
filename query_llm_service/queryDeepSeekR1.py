import os
import json
import re
import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer


# Load environment variables
load_dotenv()

# Initialize the InferenceClient
client = InferenceClient(
    provider="together",
    api_key=os.getenv("HF_ACCESS_TOKEN")
)

# System instructions for tool suggestions
system_instructions = """
- You are a smart assistant that suggests the best tools to find relevant information to answer a query from the user.
- Use the following JSON format to structure your answers:
{ "suggested_tools": [ { "tool_name": <tool_name>, "parameters": { <parameter_name>: <value> } }, ... ] }
- You have access to the following tools:

1) ORDER API ENDPOINTS:
- "GET /data" - Retrieves all records.
- "GET /data/customer/{customer_id}" - Retrieves all records for a specific customer ID.
- "GET /data/product-category/{category}" - Retrieves all records for a specific product category.
- "GET /data/order-priority/{priority}" - Retrieves all orders with a specific priority level.
- "GET /data/total-sales-by-category" - Retrieves total sales grouped by product category.
- "GET /data/high-profit-products" - Retrieves products above a specified profit threshold. takes a 'min_profit' argument.
- "GET /data/shipping-cost-summary" - Retrieves the average, minimum, and maximum shipping cost.
- "GET /data/profit-by-gender" - Retrieves total profit by customer gender.

2) PRODUCT DATABASE DOCUMENT RETRIEVAL FUNCTION:
- retrieveDocuments(query, k) - Retrieves the top k documents most relevant to the query from the database.

*IMPORTANT: You must not execute the tools, only suggest their usage*
*IMPORTANT: Always use the argument values, never use placeholders. Plug in the parameters in your response*
*IMPORTANT: Once you know which tools to use, stop thinking and give your response*
"""

# Helper function to extract response data as a serializable dictionary
def format_response(response):
    return {
        "status_code": response.status_code,
        "data": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text
    }

# Tool functions
def get_data():
    url = os.getenv('MOCK_API_URL')
    response = requests.get(url)
    return format_response(response)

def get_customer_data(customer_id):
    url = f"{os.getenv('MOCK_API_URL')}/customer/{customer_id}"
    response = requests.get(url)
    return format_response(response)

def get_product_category_data(category):
    url = f"{os.getenv('MOCK_API_URL')}/product-category/{category}"
    response = requests.get(url)
    return format_response(response)

def get_order_priority_data(priority):
    url = f"{os.getenv('MOCK_API_URL')}/order-priority/{priority}"
    response = requests.get(url)
    return format_response(response)

def get_total_sales_by_category():
    url = f"{os.getenv('MOCK_API_URL')}/total-sales-by-category"
    response = requests.get(url)
    return format_response(response)

def get_high_profit_products(min_profit):
    url = f"{os.getenv('MOCK_API_URL')}/high-profit-products"
    response = requests.get(url, params={"min_profit": min_profit})
    return format_response(response)

def get_shipping_cost_summary():
    url = f"{os.getenv('MOCK_API_URL')}/shipping-cost-summary"
    response = requests.get(url)
    return format_response(response)

def get_profit_by_gender():
    url = f"{os.getenv('MOCK_API_URL')}/profit-by-gender"
    response = requests.get(url)
    return format_response(response)

def retrieve_documents(query, k):
    # TODO: IMPLEMENT CHROMADB SIMILARITY SEARCH AGAINST QUERY, RETURN TOP K DOCUMENTS
    return [{"title": "The most relevant document", "content": "This contains all the requested information and more..."}]

# Function mapping
tool_mapping = {
    "GET /data": lambda: get_data(),
    "GET /data/customer/{customer_id}": lambda params: get_customer_data(params["customer_id"]),
    "GET /data/product-category/{category}": lambda params: get_product_category_data(params["category"]),
    "GET /data/order-priority/{priority}": lambda params: get_order_priority_data(params["priority"]),
    "GET /data/total-sales-by-category": lambda: get_total_sales_by_category(),
    "GET /data/high-profit-products": lambda params: get_high_profit_products(params["min_profit"]),
    "GET /data/shipping-cost-summary": lambda: get_shipping_cost_summary(),
    "GET /data/profit-by-gender": lambda: get_profit_by_gender(),
    "retrieveDocuments": lambda params: retrieve_documents(params["query"], params["k"]),
}

def crop_context(text, max_tokens=512):
    """
    Crops the input text so that its tokenized representation does not exceed max_tokens.
    """
    # Load a tokenizer appropriate for your model. Replace "gpt2" with your model's tokenizer if needed.
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    
    # Tokenize the input text.
    tokens = tokenizer.encode(text)
    
    # Truncate tokens if necessary.
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    
    # Decode the tokens back to a string.
    cropped_text = tokenizer.decode(tokens, skip_special_tokens=True)
    print("cropped_text:")
    print(cropped_text)
    return cropped_text

# Example usage in your summarization function:
def summarize_context(context_text, max_tokens=200):
    # Crop the context before sending to the LLM to avoid oversized input.
    cropped_context = crop_context(context_text, max_tokens=8000)  # Adjust max_tokens as needed

    summarization_prompt = (
        f"Please summarize the following context in a concise manner, "
        f"highlighting only the key details:\n\n{cropped_context}\n\nSummary:"
    )
    messages = [{"role": "user", "content": summarization_prompt}]
    
    summary_completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",
        messages=messages,
        max_tokens=max_tokens
    )
    summary_text = summary_completion.choices[0].message["content"]
    return summary_text.strip()

def generate_final_answer(user_query, tool_results):
    """
    Builds a final prompt that incorporates the original query and the tool results.
    If the tool results are too large, it summarizes the context before forming the final prompt.
    Then it sends the prompt to the LLM to obtain a final answer.
    """
    # Convert tool_results into a formatted JSON string to serve as context.
    context = json.dumps(tool_results, indent=2)
    
    # Define a threshold for the maximum allowed context length.
    # Test out different values
    CONTEXT_LENGTH_THRESHOLD = 500
    
    if len(context) > CONTEXT_LENGTH_THRESHOLD:
        print("Context too large, summarizing...")
        context = summarize_context(context, max_tokens=8000)
    
    # Build the final prompt.
    final_prompt = (
        f"Use the information in the context to answer the user query.\n\n"
        "*Always structure your answer by saying which tools were used and what information you got from them summarized in a concise way to answer the query*"
        f"Query: {user_query}\n\n"
        f"Context: {context}\n\n"
        "Answer:"
    )
    messages = [{"role": "user", "content": final_prompt}]
    
    # Query the LLM for the final answer.
    final_completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",
        messages=messages,
        max_tokens=10000
    )
    final_answer = final_completion.choices[0].message["content"]
    return final_answer

# Core LLM query logic
def process_query(user_query):
    print("processing query...")
    # Format query for LLM to suggest tools.
    formatted_query = (
        f"Follow the instructions\n"
        f"instructions:{system_instructions}\n"
        f"query:{user_query}"
    )
    messages = [{"role": "user", "content": formatted_query}]

    # Query LLM for tool suggestions.
    print("suggesting tools...")
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",
        messages=messages,
        max_tokens=500
    )

    # Extract the initial LLM response containing tool suggestions.
    response_text = completion.choices[0].message["content"]
    print(f"llm response text: \n{response_text}")

    # Parse tool suggestions from the LLM response.
    print("extracting suggested tools...")
    suggested_tools = extract_suggested_tools(response_text)

    # Execute the suggested tools.
    print("executing tools...")
    print(f"suggested tools: {suggested_tools}")
    results = execute_tools(suggested_tools)

    # Generate the final answer by using tool results as context.
    final_answer = generate_final_answer(user_query, results)

    return {
        "llm_response": response_text,
        "tool_results": results,
        "answer": final_answer
    }

# Extract suggested tools from LLM response
def extract_suggested_tools(response_text):
    # First, try to match the JSON block when it is enclosed in triple backticks.
    pattern_with_ticks = r'</think>\s*```json\s*(\{.*?\})\s*```'
    match = re.search(pattern_with_ticks, response_text, re.DOTALL)
    if match:
        try:
            parsed_json = json.loads(match.group(1))
            return parsed_json.get("suggested_tools", [])
        except json.JSONDecodeError as e:
            print("JSON decoding error (with ticks):", e)
    
    # Fallback: try to capture a JSON object after </think> even without the backticks.
    pattern_without_ticks = r'</think>\s*(\{.*\})'
    match = re.search(pattern_without_ticks, response_text, re.DOTALL)
    if match:
        try:
            parsed_json = json.loads(match.group(1))
            return parsed_json.get("suggested_tools", [])
        except json.JSONDecodeError as e:
            print("JSON decoding error (without ticks):", e)
    
    return []


# Execute suggested tools
def execute_tools(suggested_tools):
    results = {}
    for tool in suggested_tools:
        tool_name = tool.get("tool_name")
        params = tool.get("parameters", {})

        if tool_name in tool_mapping:
            try:
                if not params:  # Check if params is empty (or otherwise falsy)
                    results[tool_name] = tool_mapping[tool_name]()
                else:
                    results[tool_name] = tool_mapping[tool_name](params)
            except Exception as e:
                results[tool_name] = {"error": str(e)}
        else:
            results[tool_name] = {"error": f"Unknown tool: {tool_name}"}

    return results

