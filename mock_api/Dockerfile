FROM python:3.11-slim

ARG MOCK_API_PORT

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
COPY . .

CMD ["sh", "-c", "uvicorn mock_api:app --host 0.0.0.0"]
