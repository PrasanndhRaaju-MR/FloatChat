import pandas as pd

def load_argo_index(path="../data/raw/ArgoFloats-index.csv"):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date_update'] = pd.to_datetime(df['date_update'], errors='coerce')
    return df

if __name__ == "__main__":
    df = load_argo_index()
    print(df.head())
