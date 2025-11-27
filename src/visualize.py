import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_temp_salinity_by_float(csv_path="data/processed/argo_clean.csv"):
    # Load dataset
    df = pd.read_csv(csv_path)

    # Convert to numeric, coerce errors
    df['salinity'] = pd.to_numeric(df['salinity'], errors='coerce')
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')

    # Check if salinity exists
    has_salinity = df['salinity'].notna().any()

    floats = df['float_file'].unique()
    colors = sns.color_palette("tab10", len(floats))

    plt.figure(figsize=(12, 7))

    for i, f in enumerate(floats):
        df_float = df[df['float_file'] == f]
        df_float = df_float.dropna(subset=['temperature', 'pressure'])  # always need temp & pres

        if has_salinity:
            df_float = df_float.dropna(subset=['salinity'])
            plt.scatter(
                df_float['salinity'],
                df_float['temperature'],
                c=[colors[i]] * len(df_float),
                label=f.split('/')[-1],
                alpha=0.6,
                s=40
            )
            plt.xlabel("Salinity (psu)")
            plt.ylabel("Temperature (°C)")
            plt.title("TS Diagram by Float from Argo Profiles")
        else:
            # If no salinity, plot Temperature vs Pressure
            plt.plot(
                df_float['temperature'],
                df_float['pressure'],
                marker='o',
                linestyle='-',
                color=colors[i],
                label=f.split('/')[-1]
            )
            plt.xlabel("Temperature (°C)")
            plt.ylabel("Pressure (dbar)")
            plt.title("Temperature vs Pressure by Float (Salinity missing)")

    plt.gca().invert_yaxis()  # Depth/pressure increases downward
    plt.legend(title="Float Files", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_temp_salinity_by_float()
