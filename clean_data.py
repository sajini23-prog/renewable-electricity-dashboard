import pandas as pd

# Load raw dataset
file_path = "data/API_EG.ELC.RNEW.ZS_DS2_en_csv_v2_6648.csv"
df = pd.read_csv(file_path, skiprows=4)

# Keep identifier columns
id_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]

# Reshape from wide to long format
df_long = df.melt(
    id_vars=id_columns,
    var_name="Year",
    value_name="Renewable Output"
)

# Remove missing renewable output values
df_long = df_long.dropna(subset=["Renewable Output"])

# Convert Year to numeric
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")
df_long = df_long.dropna(subset=["Year"])
df_long["Year"] = df_long["Year"].astype(int)

# Keep zeros because they may be valid values
# Remove aggregate rows by using country code length = 3 and excluding common aggregate codes if needed
df_long = df_long[df_long["Country Code"].str.len() == 3]

# List of aggregate codes commonly found in World Bank datasets
aggregate_codes = [
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS",
    "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
    "INX", "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC",
    "MNA", "NAC", "OED", "OSS", "PRE", "PSS", "PST", "SAS", "SSA", "SSF",
    "SST", "TEA", "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD"
]

df_final = df_long[~df_long["Country Code"].isin(aggregate_codes)]

# Save final cleaned country-level dataset
output_path = "data/final_renewable_electricity.csv"
df_final.to_csv(output_path, index=False)

print("Final cleaned dataset saved successfully.")
print("Shape:", df_final.shape)
print("Columns:", df_final.columns.tolist())
print(df_final.head())