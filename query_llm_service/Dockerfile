FROM python:3.11-slim

ARG LLM_SERVICE_PORT

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
COPY . .

EXPOSE ${LLM_SERVICE_PORT}

CMD ["sh", "-c", "uvicorn llm_server:app --host 0.0.0.0 --port ${LLM_SERVICE_PORT}"]

