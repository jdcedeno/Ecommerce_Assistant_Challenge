import argparse
import json
from dotenv import load_dotenv
import os
import time
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Set up Hugging Face Inference Client with API key from environment variables
client = InferenceClient(api_key=os.getenv("HF_ACCESS_TOKEN"))

# Tool definitions
def retrieve_order_details(customer_id: str) -> str:
    """
    Retrieve order details for a given customer ID.
    """
    time.sleep(3)  # Simulate API delay
    return f"id={customer_id},date=01/07/2025,total=$150,product='we make it happen t-shirt'"

def retrieve_product_details(query: str, k: int) -> str:
    """
    Retrieve documents related to product information.
    """
    time.sleep(3)
    documents = [
        f"product_id=10,product_name='we make it happen t-shirt',product_type=men's clothing,price=$250,discount=$100",
        f"product_id=11,product_name='we make it happen hoodie sweater',product_type=men's clothing,price=$350,discount=$100",
        f"product_id=22,product_name='we make it happen tall socks pair',product_type=underwear,price=$30,discount=$0",
        f"product_id=23,product_name='we make it happen short socks pair',product_type=underwear,price=$30,discount=$0",
        f"product_id=34,product_name='we make it happen silk underwear',product_type=underwear,price=$80,discount=$0",
    ]
    return "\n".join(documents)

def execute_tools(llm_response: str) -> dict:
    """
    Execute the tools specified in the LLM response and return results.
    """
    results = {}

    if "CALL retrieve_order_details" in llm_response:
        customer_id = llm_response.split("customer_id=")[-1].split(")")[0].strip("' ")
        results["retrieve_order_details"] = {
            "parameters": {"customer_id": customer_id},
            "result": retrieve_order_details(customer_id)
        }

    if "CALL retrieve_product_details" in llm_response:
        query = llm_response.split("query=")[-1].split(",")[0].strip("' ")
        k = int(llm_response.split("k=")[-1].split(")")[0])
        results["retrieve_product_details"] = {
            "parameters": {"query": query, "k": k},
            "result": retrieve_product_details(query, k)
        }

    return results

def main():
    parser = argparse.ArgumentParser(description="Tool picker script that queries an LLM for tool execution.")
    parser.add_argument("query", type=str, help="The query to be processed by the LLM")
    args = parser.parse_args()

    user_query = args.query
    
    conversation = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant with access to the following tools:\n\n"
                "1. retrieve_order_details(customer_id: str): Retrieves order details for a given customer ID.\n"
                "Example: CALL retrieve_order_details(customer_id='12345')\n\n"
                "2. retrieve_product_details(query: str, k: int): Retrieves product information based on a query.\n"
                "Example: CALL retrieve_product_details(query='laptop', k=5), k is the number of related documents to retrieve\n\n"
                "If a query cannot be answered using the tools, provide a general response."
            )
        },
        {"role": "user", "content": user_query}
    ]

    # Call LLaMA inference API
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=conversation,
        max_tokens=500
    )

    # Extract model response
    response_text = completion.choices[0].message['content']

    # Parse and execute tools based on response
    tool_results = execute_tools(response_text)
    print(json.dumps(tool_results, indent=2))

if __name__ == "__main__":
    main()
