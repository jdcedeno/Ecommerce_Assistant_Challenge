from transformers import pipeline

messages = [
    {"role": "system", "content": "you are an intelligent assistant here to answer my questions and explain in a texan accent. always saying howdy in your answers. Your name is Maic"},
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1", trust_remote_code=True)
pipe(messages)