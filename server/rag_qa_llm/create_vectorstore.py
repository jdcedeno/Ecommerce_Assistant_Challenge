import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


print("LOADING PRODUCT AND ORDER DATA...")
product_data = pd.read_csv("./data/product_data_clean.csv", encoding="utf-8", sep=",", quotechar='"', dtype=str)

print("LOADING HUGGINGFACE EMBEDDINGS...")
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("PROCESSING DATA...")
data_texts = product_data.apply(lambda row: " ".join(row.values.astype(str)), axis=1)

print("LOADING VECTORSTORE FROM PERSIST DIRECTORY...")
vectorstore = Chroma.from_texts(texts= data_texts, persist_directory="./vectorstore", embedding=hf_embeddings)