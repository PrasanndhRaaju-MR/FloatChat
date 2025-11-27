# src/fetch_profiles.py
import os
import requests
import xarray as xr

# ✅ Define GDAC mirrors at the top
GDAC_MIRRORS = [
    "https://data-argo.ifremer.fr/dac/"
]

def download_profile(file_path, save_dir="../data/raw/profiles"):
    os.makedirs(save_dir, exist_ok=True)
    local_path = os.path.join(save_dir, os.path.basename(file_path))

    if os.path.exists(local_path):
        print(f"✅ Already exists: {local_path}")
        return local_path

    for base in GDAC_MIRRORS:
        url = base + file_path
        print(f"🔎 Trying {url} ...")
        try:
            r = requests.get(url, stream=True, timeout=60)
            if r.status_code == 200:
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ Downloaded from {base}")
                return local_path
            else:
                print(f"❌ Not found at {base} (status {r.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error with {base}: {e}")

    raise RuntimeError(f"Profile {file_path} not found on any GDAC mirror")

def parse_profile(nc_path):
    ds = xr.open_dataset(nc_path)

    def safe_get(var):
        return ds[var].values.flatten() if var in ds.variables else None

    return {
        "PRES": safe_get("PRES"),
        "TEMP": safe_get("TEMP"),
        "PSAL": safe_get("PSAL"),  # may be None
    }

if __name__ == "__main__":
    from load_index import load_argo_index
    df = load_argo_index()
    for idx, row in df.iterrows():
        file_path = row["file"]
        if not isinstance(file_path, str) or file_path.strip() == "":
            continue
        try:
            print(f"=== Processing profile {idx + 1}: {file_path} ===")
            nc_path = download_profile(file_path)
            data = parse_profile(nc_path)
            print(data)
        except Exception as e:
            print(f"❌ Error with {file_path}: {e}")
