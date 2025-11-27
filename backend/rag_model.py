import os
import google.generativeai as genai
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class RAGModel:
    def __init__(self, db_params):
        self.db_params = db_params
        # Configure Gemini API
        genai.configure(api_key="API KEY")
        self.client = genai.GenerativeModel('gemini-2.0-flash')

    def _get_db_schema(self):
        """
        Provide a simple database schema for the LLM to understand.
        All semantic matching is done via the 'summary' field.
        """
        return {
            "table": "profiles",
            "columns": [
                "profile_id", "date_time", "latitude", "longitude",
                "summary", "ocean", "institution"
            ],
            "description": (
                "Table containing metadata for ARGO float profiles. "
                "Only the 'summary' field should be used for semantic matching. "
                "Optional filters: latitude, longitude, date_time, and ocean."
            )
        }

    def generate_sql(self, user_query: str):
        """
        Generate a SQL query from natural language using Gemini API.
        """
        context_payload = {
            "system_prompt": """You are an SQL generator for the Argo float database.
Only generate SELECT queries.
Never include DROP, DELETE, UPDATE, or other destructive commands.
Limit results to 100 rows.
All semantic matching should be done on the 'summary' field.
Optional filters: latitude, longitude, date_time, and ocean.""",
            "db_schema": self._get_db_schema(),
            "user_query": user_query
        }

        prompt = f"""
{context_payload['system_prompt']}
---
Database Schema:
{context_payload['db_schema']}
---
User Query: "{context_payload['user_query']}"
---
Generate ONLY the PostgreSQL query, without markdown, explanation, or extra text.
        """

        try:
            response = self.client.generate_content(prompt)
            sql_query = response.text.strip()

            # Remove any Markdown code fences
            sql_query = sql_query.replace("```sql", "").replace("```python", "").replace("```", "").strip()
            return sql_query

        except Exception as e:
            print(f"❌ Error with Gemini API: {e}")
            return None

    def execute_sql(self, sql_query: str):
        """
        Execute the generated SQL query on the PostgreSQL database.
        """
        if not sql_query:
            return {"error": "No SQL query provided."}

        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()
            cur.execute(sql_query)
            results = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in results]

        except (psycopg2.Error, ValueError) as e:
            print(f"❌ SQL execution failed: {e}")
            return {"error": str(e)}

        finally:
            if conn:
                cur.close()
                conn.close()
