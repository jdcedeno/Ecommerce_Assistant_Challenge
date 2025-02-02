from dotenv import load_dotenv
import sys
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import torch


load_dotenv()

def generate_response(user_query):
    # Tokenize the input query
    inputs = tokenizer(user_query, return_tensors="pt").to("cuda")

    # Generate the model's response
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512, temperature=0.6)

    # Decode the generated tokens back to text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py 'Your query here'")
        sys.exit(1)

    user_query = sys.argv[1]

    # Load the tokenizer and model
    model_name = "deepseek-ai/DeepSeek-R1"
    config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
    config.quantization_config = None
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, config=config, device_map="auto", trust_remote_code=True, cache_dir="D:/huggingface_cache")

    # Generate and print the response
    response = generate_response(user_query)
    print("Model response:", response)
