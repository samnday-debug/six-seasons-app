import pandas as pd

files = {
    "max_temp": "data/Station_009021_Max_Temp_Data.csv",
    "min_temp": "data/Station_009021_Min_Temp_Data.csv",
    "rainfall": "data/Station_009021_Rainfall_Data.csv",
}

for name, path in files.items():
    df = pd.read_csv(path)
    print(f"\n===== {name} =====")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print(df.head(3))
    print("Missing values per column:")
    print(df.isna().sum())