from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pandas as pd

from rag_model import RAGModel  

app = FastAPI()

# -------------------------
# Database connection parameters
# -------------------------
db_params = {
    'dbname': 'argo_db',
    'user': 'postgres',
    'password': '1358',
    'host': 'localhost',
    'port': '5432'
}

# Initialize RAG Model
rag_model = RAGModel(db_params)

# -------------------------
# Request Model
# -------------------------
class Query(BaseModel):
    question: str

# -------------------------
# Chat Endpoint
# -------------------------
@app.post("/chat")
def chat(q: Query):
    """Translates user query into SQL and returns results from PostgreSQL."""
    sql_query = rag_model.generate_sql(q.question)

    if not sql_query:
        raise HTTPException(status_code=500, detail="Failed to generate SQL query.")

    print(f"Generated SQL: {sql_query}")

    results = rag_model.execute_sql(sql_query)
    if "error" in results:
        return {
            "response": f"I'm sorry, I couldn't process that query. Database error: {results['error']}"
        }

    return {
        "response": "Here are the profiles that match your request:",
        "results": results
    }

# -------------------------
# Profiles Endpoint
# -------------------------
@app.get("/profiles/{profile_id}")
def get_profile_data(profile_id: str):
    """
    Fetches full depth-series (PRES, TEMP, PSAL) for a given profile from Parquet file.
    Assumes parquet files are saved in ./profiles_data/{profile_id}.parquet
    """
    try:
        parquet_dir = "./profiles_data"
        parquet_file = os.path.join(parquet_dir, f"{profile_id}.parquet")

        if not os.path.exists(parquet_file):
            raise HTTPException(status_code=404, detail=f"Profile data not found for ID {profile_id}")

        df = pd.read_parquet(parquet_file)

        # Select only depth-series columns if present
        depth_series = df[["PRES", "TEMP", "PSAL"]].to_dict(orient="records")

        return {
            "profile_id": profile_id,
            "depth_series": depth_series
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading profile data: {str(e)}")
