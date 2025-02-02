from fastapi import FastAPI, Request
from queryDeepSeekR1 import process_query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello! FastAPI is running for llm query."}

@app.post("/query")
async def query_llm(request: Request):
    data = await request.json()
    user_query = data

    if not user_query:
        return {"error": "Query is required."}

    # Process the query using LLM and tools
    result = process_query(user_query)
    return result
