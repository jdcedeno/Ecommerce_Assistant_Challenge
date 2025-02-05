# Instructions
1. Create a .env file with the following variables:
```
VITE_API_URL="http://localhost:<same-as-server-port>"
CLIENT_PORT=<for-example-3000>
SERVER_PORT=<for-example-3001>
LLM_SERVICE_URL="http://query_llm_service:8000"
HF_ACCESS_TOKEN=<your_pro_plan_huggingface_access_token>
MOCK_API_URL="http://mock_api:8000/data"
```
2. Run docker compose -f docker-compose.yml --env-file .env up -d --build

3. Access localhost:<CLIENT_PORT> to visit the client and make queries to the assistant
