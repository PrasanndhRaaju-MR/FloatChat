import os
import pandas as pd
import psycopg2
from chromadb import Client, Settings
from chromadb.utils import embedding_functions

# Base directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "vector_db")
COLLECTION_NAME = "argo_profiles"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def build_vector_index(db_params={}):
    """Builds a ChromaDB vector index from PostgreSQL profile summaries."""
    default_db_params = {
        'dbname': 'argo_db',
        'user': 'postgres',
        'password': '1358',
        'host': 'localhost',
        'port': '5432'
    }
    db_params = {**default_db_params, **db_params}

    try:
        conn = psycopg2.connect(**db_params)
        sql = "SELECT profile_id, summary FROM profiles WHERE summary IS NOT NULL;"
        df = pd.read_sql(sql, conn)
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed. Error: {e}")
        return

    if df.empty:
        print("⚠️ No summaries found in the database to index.")
        return

    # Ensure vector_db directory exists
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

    client = Client(Settings(persist_directory=PERSIST_DIRECTORY))
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )

    # Create collection if it doesn’t exist
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )
    except Exception:
        collection = client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )

    # Add documents and IDs
    collection.add(
        documents=df["summary"].tolist(),
        ids=df["profile_id"].astype(str).tolist()
    )

    print(f"✅ Vector index built with {len(df)} profiles at {PERSIST_DIRECTORY}")

if __name__ == "__main__":
    build_vector_index()
