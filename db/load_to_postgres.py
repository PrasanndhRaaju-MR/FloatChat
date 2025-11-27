import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import warnings

# Suppress the UserWarning from pandas
warnings.filterwarnings("ignore", category=UserWarning)

# Map single-letter ocean codes to full names
OCEAN_MAP = {
    "A": "Atlantic",
    "I": "Indian",
    "P": "Pacific",
    "S": "Southern",
    "N": "Arctic"
}

def load_data_to_postgres(csv_path="../data/processed/argo_clean.csv", db_params={}):
    """Loads cleaned data from a CSV into a PostgreSQL database with enriched summaries."""
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Error: {csv_path} not found. Please run the preprocessing script first.")
        return

    # Basic cleanup and data type conversion
    df = df.rename(columns={
        'date': 'date_time',
        'lat': 'latitude',
        'lon': 'longitude'
    })
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce', utc=True)
    df['date_update'] = pd.to_datetime(df.get('date_update', pd.NaT), errors='coerce', utc=True)

    # Normalize ocean codes
    df['ocean'] = df['ocean'].map(OCEAN_MAP).fillna(df['ocean'])

    # Drop invalid rows
    df = df.dropna(subset=['date_time', 'latitude', 'longitude'])

    # Deduplicate by float_file + timestamp
    df_meta = df.drop_duplicates(subset=['float_file', 'date_time'])

    # Enriched summary generator
    def create_summary(row):
        date_update_str = (
            row['date_update'].strftime('%Y-%m-%d %H:%M:%S UTC')
            if pd.notna(row.get('date_update')) else "unknown"
        )
        return (
            f"Profile from float {row.get('profiler_type', 'unknown')} "
            f"deployed by institution {row.get('institution', 'unknown')} "
            f"collected on {row['date_time'].strftime('%Y-%m-%d %H:%M:%S')} UTC "
            f"in the {row.get('ocean', 'unknown')} Ocean at "
            f"latitude {row['latitude']:.2f}° and longitude {row['longitude']:.2f}°. "
            f"Profiler type: {row.get('profiler_type', 'N/A')}. "
            f"Contains measurements of temperature and salinity. "
            f"Last updated on {date_update_str}."
        )

    df_meta['summary'] = df_meta.apply(create_summary, axis=1)

    # Replace NaT with None before inserting
    df_meta['date_update'] = df_meta['date_update'].where(pd.notna(df_meta['date_update']), None)

    # Add a simple profile_id as it might not be in the CSV
    df_meta['profile_id'] = (
        df_meta['float_file'].apply(lambda x: x.split('/')[-1].replace('.nc', ''))
        + '_' + df_meta.index.astype(str)
    )

    # Use your database connection parameters
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
        cur = conn.cursor()

        # Insert into the profiles table
        print(f"📥 Loading {len(df_meta)} unique profiles into PostgreSQL...")

        insert_query = """
        INSERT INTO profiles (
            profile_id, float_file, date_time, latitude, longitude, geom,
            ocean, institution, profiler_type, summary, date_update
        ) VALUES %s
        """

        values = [(
            row['profile_id'],
            row['float_file'],
            row['date_time'],
            row['latitude'],
            row['longitude'],
            f"POINT({row['longitude']} {row['latitude']})",  # PostGIS geometry
            row.get('ocean', None),
            row.get('institution', None),
            row.get('profiler_type', None),
            row['summary'],
            row['date_update'] if pd.notna(row.get('date_update')) else None
        ) for _, row in df_meta.iterrows()]

        execute_values(cur, insert_query, values)
        conn.commit()
        print("✅ Data loaded successfully!")

    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed. Please ensure your PostgreSQL is running and credentials are correct. Error: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    load_data_to_postgres()
