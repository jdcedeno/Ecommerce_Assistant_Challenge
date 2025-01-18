import argparse
import chromadb
from sentence_transformers import SentenceTransformer

parser = argparse.ArgumentParser(description="a script to query and optionally reset and re-create a chromadb collection")
parser.add_argument("--reset", action="store_true")
parser.add_argument("query", type=str)
args = parser.parse_args()

client = chromadb.HttpClient(host="localhost",port=8000)

model_name = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(model_name)

collection_name = "fruits"
if collection_name in client.list_collections() and args.reset is True:
    client.delete_collection(collection_name)

    print(f"creating collection {collection_name}...")
    collection = client.get_or_create_collection(collection_name)

    ids = ["lemon", "pineapple", "strawberry", "orange"]
    metadatas = [{"tags": "green, acid, round, small, fits in the palm of one hand, used for treating flu and cold symptoms"}, 
                {"tags": "yellow, acid and sweet, pizza topping, large, difficult to carry with one hand, has small spikes"}, 
                {"tags": "red, sweet, good ingredient for desserts and smoothies, very small, heart-shaped, the little seeds look like a beard"},
                {"tags": "orange, round, the size of a baseball, good for desserts, salad dressings, marinades, juice, it's a very versatile fruit"}]
    documents = ["Facts: Lemons are rich in vitamin C, antioxidants, and citric acid, which aids digestion and boosts immunity. They are widely used in beverages, cooking, and cleaning products. The peel contains essential oils used in perfumes and aromatherapy. Historic/Cultural Fact: Originating in Asia, lemons were introduced to Europe around the 1st century AD via Roman trade routes. They became a symbol of wealth in the Mediterranean during the Renaissance.",
                "Facts: Pineapples are high in bromelain, an enzyme aiding digestion, and are a good source of vitamins C and B6. Their spin skin protects the juicy, sweet interior. Pineapples do not ripen after being picked. Historic/Cultural Fact: Native to South America, pineapples were brought to Europe by Christopher Columbus in 1493. They becam a status symbol in colonial times due to their rarity and cost.",
                "Facts: Strawberries are packed with vitamin C, fiber, and antioxidants. They are the only fruit with seeds on the outside and are technically aggregate fruits, not berries. Historic/Cultural Fact: Strawberries were cultivated as early as the Roman era but gained prominence in the 18th century in France, where modern garden strawberries were first bred.",
                "Facts: Oranges are a top source of vitamin C, providing immune support and hydration. They are a hybrid of pomelo and mandarin and are grown in tropical and subtropical climates. Historic/Cultural Fact: Oranges originated in Southeast Asia and were brought to the Mediterranean region by Arab traders around the 10th century, becoming a staple in European cuisine."]

    embeddings = embedding_model.encode(documents)

    collection.add(ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings)
    print("collection created!")

query = args.query
print(f"query is: {query}")
query_embeddings = embedding_model.encode(query)
collection = client.get_collection(collection_name)
results = collection.query(query_embeddings=query_embeddings, n_results=3)
print("results...")
print(results)