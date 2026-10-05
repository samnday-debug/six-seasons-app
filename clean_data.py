"""Clean and merge the three BOM files into one daily CSV."""
import pandas as pd

DATA = "data/"

def load_bom(path, value_col, period_col, new_name):
    """Load one BOM file and keep just the date, value and quality."""
    df = pd.read_csv(path)

    # 1. Build a proper date from the Year/Month/Day columns
    df["date"] = pd.to_datetime(df[["Year", "Month", "Day"]])

    # 2. Blank period/accumulation means a normal 1-day reading
    df[period_col] = df[period_col].fillna(1)

    # 3. If one value covers several days, it's not a true daily reading -> blank it
    multi_day = df[period_col] > 1
    print(f"{new_name}: {multi_day.sum()} multi-day readings set to missing")
    df.loc[multi_day, value_col] = None

    # 4. Keep only what we need, with simple column names
    df = df[["date", value_col, "Quality"]]
    df = df.rename(columns={value_col: new_name, "Quality": f"{new_name}_quality"})
    return df


max_t = load_bom(DATA + "Station_009021_Max_Temp_Data.csv",
                 "Maximum temperature (Degree C)",
                 "Days of accumulation of maximum temperature", "max_temp_c")
min_t = load_bom(DATA + "Station_009021_Min_Temp_Data.csv",
                 "Minimum temperature (Degree C)",
                 "Days of accumulation of minimum temperature", "min_temp_c")
rain = load_bom(DATA + "Station_009021_Rainfall_Data.csv",
                "Rainfall amount (millimetres)",
                "Period over which rainfall was measured (days)", "rainfall_mm")

# 5. Merge the three on date (outer = keep a date even if only one file has it)
df = max_t.merge(min_t, on="date", how="outer").merge(rain, on="date", how="outer")

# 6. Drop days where ALL three values are missing (e.g. before records started)
before = len(df)
df = df.dropna(subset=["max_temp_c", "min_temp_c", "rainfall_mm"], how="all")
print(f"Dropped {before - len(df)} completely empty days")

# 7. Sanity checks
assert len(df) >= 200, "Need at least 200 records"
assert df["date"].is_unique, "Duplicate dates found"
bad = df[df["min_temp_c"] > df["max_temp_c"]]
print(f"Days where min > max (suspicious): {len(bad)}")

# 8. Save
df = df.sort_values("date")
df.to_csv(DATA + "perth_daily_clean.csv", index=False)
print(f"\nSaved {len(df)} rows from {df['date'].min().date()} to {df['date'].max().date()}")
print(df.head())

print("\nFirst date with each measurement:")
for col in ["max_temp_c", "min_temp_c", "rainfall_mm"]:
    print(f"  {col}: {df.loc[df[col].notna(), 'date'].min().date()}")

print("\nUnchecked (quality 'N') values:")
for col in ["max_temp_c", "min_temp_c", "rainfall_mm"]:
    print(f"  {col}: {(df[f'{col}_quality'] == 'N').sum()}")

print("\nUnchecked max temp values by year (only years that have some):")
n_by_year = df[df["max_temp_c_quality"] == "N"].groupby(df["date"].dt.year).size()
print(n_by_year.to_string())    