import os
import pandas as pd
from fetch_profiles import download_profile, parse_profile
from load_index import load_argo_index

def build_clean_dataset():
    df_index = load_argo_index()
    
    # Drop rows where 'file' is NaN
    df_index = df_index.dropna(subset=["file"])
    records = []
    for i, row in df_index.iterrows():
        file_path = row["file"]
        if not isinstance(file_path, str):
            print(f"Skipping invalid file path: {file_path}")
            continue

        try:
            print(f"=== Processing profile {i+1}: {file_path} ===")
            nc_path = download_profile(file_path)
            profile = parse_profile(nc_path)

            pres = profile.get("PRES", [])
            temp = profile.get("TEMP", [])
            psal = profile.get("PSAL") or [None] * len(pres)  # Handle missing PSAL

            for p, t, s in zip(pres, temp, psal):
                records.append({
                    "float_file": file_path,
                    "date": row["date"],
                    "lat": row["latitude"],
                    "lon": row["longitude"],
                    "ocean": row["ocean"],
                    "profiler_type": row["profiler_type"],
                    "pressure": p,
                    "temperature": t,
                    "salinity": s
                })
                
        except Exception as e:
            print(f"❌ Error with {file_path}: {e}")
            
    df_clean = pd.DataFrame(records)
    os.makedirs("../data/processed", exist_ok=True)
    df_clean.to_csv("../data/processed/argo_clean.csv", index=False)
    print(f"✅ Saved cleaned dataset with {len(df_clean)} rows to data/processed/argo_clean.csv")
    return df_clean

if __name__ == "__main__":
    df = build_clean_dataset()
    print(df.head())