#!/usr/bin/env python3
import sys
from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

if len(sys.argv) < 2:
    print("Usage: python query_llm.py <query>")
    sys.exit(1)

query = sys.argv[1]

print("LOADING HUGGINGFACE EMBEDDINGS...")
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("LOADING VECTORSTORE FROM PERSIST DIRECTORY...")
vectorstore = Chroma(persist_directory="./vectorstore", embedding_function=hf_embeddings)

print("CREATING RETRIEVER...")
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})

print("QUERYING VECTORSTORE...")
retrieved_docs = retriever.invoke(query)
if not retrieved_docs:
    print("No relevant documents found.")
    sys.exit(1)

context = retrieved_docs[0].to_json()
context = context["kwargs"]["page_content"]

print("CREATING PIPELINE...")
qa_model_name = "deepset/roberta-base-squad2"  # Use a QA-specific model
hf_pipeline = pipeline(task="question-answering", model=qa_model_name, tokenizer=qa_model_name)

qa_input = {"question": query, "context": context}
answer = hf_pipeline(qa_input)

print("ANSWER:", answer["answer"])
print("RELATED DOCUMENTS:", retrieved_docs[0].to_json())
