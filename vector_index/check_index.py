import os
from chromadb import Client, Settings

# Base directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "vector_db")
COLLECTION_NAME = "argo_profiles"

def check_collection():
    client = Client(Settings(persist_directory=PERSIST_DIRECTORY))

    # List available collections
    print("📂 Collections available:", client.list_collections())

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"❌ Could not load collection {COLLECTION_NAME}: {e}")
        return

    print(f"📊 Number of profiles stored: {collection.count()}")

    # Peek into stored items
    sample = collection.peek(limit=5)
    print("\n🔍 Sample stored items:")
    for i, doc in enumerate(sample["documents"]):
        print(f"  {i+1}. ID={sample['ids'][i]} | Doc={doc[:80]}...")

    # Try a semantic search
    query_text = "temperature profile in the ocean"
    results = collection.query(query_texts=[query_text], n_results=3)
    print("\n🔎 Search results for query:", query_text)
    for i, doc in enumerate(results["documents"][0]):
        print(f"  Result {i+1}: ID={results['ids'][0][i]} | Doc={doc[:80]}...")

if __name__ == "__main__":
    abs_path = os.path.abspath(PERSIST_DIRECTORY)
    print(f"📁 Using persistence directory: {abs_path}\n")
    check_collection()
