import os
from chromadb import Client, Settings
from chromadb.utils import embedding_functions

# Define constants for persistence and collection names
PERSIST_DIRECTORY = "vector_db"
COLLECTION_NAME = "argo_profiles"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def get_collection():
    """
    Initializes a ChromaDB client and gets the collection.
    This function is called by `search()` on every request to ensure
    a fresh, working connection.
    """
    try:
        os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
        settings = Settings(persist_directory=PERSIST_DIRECTORY)
        client = Client(settings=settings)
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
        # We use client.get_collection here, which is the correct way
        collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)
        return collection
    except Exception as e:
        # Print the error for debugging, but don't crash
        print(f"❌ Error getting ChromaDB collection: {e}")
        return None

def search(query_text, k=5):
    """Performs a semantic search on the ChromaDB collection."""
    collection = get_collection()
    if collection is None:
        return {"ids": [], "documents": [], "metadatas": []}
    
    try:
        results = collection.query(query_texts=[query_text], n_results=k)
        return results
    except Exception as e:
        print(f"❌ Error performing vector search: {e}")
        return {"ids": [], "documents": [], "metadatas": []}

if __name__ == "__main__":
    print("This script is now a helper module. Please use build_index.py to create the index.")