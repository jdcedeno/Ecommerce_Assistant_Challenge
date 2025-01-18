# Instructions

## Deploy a Chromadb docker container (this is the recommended way of using chroma in production)
docker pull chromadb/chroma
docker run --name music-store -p 8000:8000 -d chromadb/chroma

## 