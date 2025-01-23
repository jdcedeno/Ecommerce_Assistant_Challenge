from dotenv import load_dotenv
import os
import json
import argparse
import subprocess
import platform
import requests

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": f"Bearer {os.getenv("HF_ACCESS_TOKEN")}"}

def query_roberta(question, context):
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def run_tool_picker(user_query):
    env_vars = os.environ.copy()
    env_vars["PYTHONPATH"] = os.getcwd()

    if platform.system() == "Windows":
        command = f'cmd /c "venv\\Scripts\\activate && python toolPicker.py "{user_query}""'
    else:
        command = f"bash -c 'source venv/bin/activate && python toolPicker.py \"{user_query}\"'"

    result = subprocess.run(command, capture_output=True, text=True, env=env_vars, shell=True)

    if result.returncode != 0:
        print(f"Error running toolPicker.py: {result.stderr}")
        return {}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output from toolPicker.py: {e}")
        return {}



def format_tool_results(user_query, tool_results):
    formatted_results = {}
    context_parts = []

    # Collect results from each tool
    for tool, data in tool_results.items():
        parameters = data.get("parameters", {})
        context = data.get("result", "")
        
        # Store tool results for final context
        context_parts.append(f"{tool}: {context}")

        # Add tool results to formatted output
        formatted_results[tool] = {
            "parameters": parameters,
            "context": context
        }

    # Create a single combined context for the final query
    combined_context = "\n".join(context_parts)

    # Query RoBERTa once with the full combined context
    qa_response = query_roberta(user_query, combined_context)

    # Include the final LLM response in the formatted results
    formatted_results["final_response"] = {
        "question": user_query,
        "combined_context": combined_context,
        "result": qa_response
    }

    return {"tool_calls": formatted_results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a user query through toolPicker and RoBERTa QA model.")
    parser.add_argument("query", type=str, help="The user query to be processed.")
    args = parser.parse_args()

    user_query = args.query
    tool_results = run_tool_picker(user_query)
    qa_results = format_tool_results(user_query, tool_results)

    print(json.dumps(qa_results, indent=2))
