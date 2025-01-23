# import chromadb
# from sentence_transformers import SentenceTransformer
# import pandas as pd

# # Initialize ChromaDB client
# chroma_client = chromadb.HttpClient(host="localhost", port=8000)

# # Initialize SentenceTransformer model
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# # Create a collection in ChromaDB
# collection_name = "music_products"
# collection = chroma_client.get_or_create_collection(name=collection_name)

# def load_csv_to_vectorstore(csv_path):
#     """
#     Loads data from a CSV file into the ChromaDB vector store.

#     Args:
#         csv_path (str): Path to the CSV file.
#     """
#     # Read the CSV file
#     df = pd.read_csv(csv_path)

#     # Iterate through rows and add to vector store
#     for _, row in df.iterrows():
#         # print("row: ")
#         # print(row)
#         # Prepare the ID, metadata, and document
#         title = str(row['title'])  # Use title as ID
#         # print("title: ")
#         # print(title)
#         metadata = row.drop(['title', 'description']).to_dict()  # Use other columns as metadata
#         # print("metadata: ")
#         # print(metadata)

#         document = row['description']  # Assuming 'description' contains the main text
#         # print("document: ")
#         # print(document)
#         # Add the row to the ChromaDB collection
#         collection.add(
#             ids=[title],
#             documents=[document],
#             metadatas=[metadata]
#         )

# # def search_music_products(query, top_k=5):
# #     """
# #     Searches for similar products in the vector store based on the query.

# #     Args:
# #         query (str): The search query.
# #         top_k (int): Number of top results to return.

# #     Returns:
# #         list: List of matched products.
# #     """
# #     query_embedding = embedding_model.encode(query)
# #     results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

# #     return results

# # Example usage
# csv_path = "./data/product_data_clean.csv"  # Path to your CSV file
# load_csv_to_vectorstore(csv_path)
# print("collection")
# print(collection)
# print("collection.get()")
# print(collection.get(limit=3))

# # Example query
# # query = "best guitar for beginners"
# # results = search_music_products(query)

# # # Display results
# # print("Search Results:")
# # for result, metadata in zip(results["ids"], results["metadatas"]):
# #     print(f"ID: {result}, Title: {metadata['title']}, Description: {metadata['description']}, Price: {metadata['price']}")
