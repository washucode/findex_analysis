import pandas as pd
import numpy as np

# --------------------------
# 1. LOAD DATA
# --------------------------
df_raw = pd.read_excel("findex_2025.xlsx")   # or .csv
print("Rows:", len(df_raw))
print("Columns:", len(df_raw.columns))


# --------------------------
# 2. DEFINE COLUMN GROUPS
# --------------------------

identifier_cols = [
    "economy", "regionwb"
]

demographic_cols = [
    "female", "age", "educ", "urbanicity", "inc_q", "emp_in"
]

finclusion_cols = [
    "account", "account_fin", "account_mob",
    "dig_account", "anydigpayment"
]

entrepreneur_cols = [
    "fin17a", "fin17b", "fin18", "fin20", "fin21", "fin22e"
]

barrier_cols = [
    "fin11a","fin11b","fin11c","fin11d","fin11f",
    "fin14a","fin14b","fin14c","fin14d","fin14e"
]

digital_cols = [
    "con1", "con12", "con25", "con30c", "con30g"
]

payment_behavior_cols = [
    "borrowed", "saved", "receive_wages",
    "receive_transfers", "receive_pensions",
    "receive_agriculture", "merchantpay_dig",
    "pay_utilities", "domestic_remittances"
]

# Combine all
columns_to_keep = (
    identifier_cols +
    demographic_cols +
    finclusion_cols +
    entrepreneur_cols +
    barrier_cols +
    digital_cols +
    payment_behavior_cols
)

# SAFELY SELECT (avoids KeyErrors)
available_cols = [c for c in columns_to_keep if c in df_raw.columns]
df = df_raw[available_cols].copy()

print("Using", len(available_cols), "columns.")


# --------------------------
# 3. CLEAN BASIC CODES
# --------------------------

# Convert missing codes
df = df.replace(["..", " ", "", "NA", "N/A", 998, 999], np.nan)


# --------------------------
# 4. CLEAN GENDER
# --------------------------
if "female" in df.columns:
    df["gender"] = df["female"].map({1: "Female", 2: "Male"})
    df.drop(columns=["female"], inplace=True)


# --------------------------
# 5. CLEAN EMPLOYMENT
# --------------------------
if "emp_in" in df.columns:
    employment_map = {
        1: "In Labor Force",
        2: "Not in Labor Force",
        98: "Don't Know",
        99: "Refused"
    }
    df["employment_status"] = df["emp_in"].map(employment_map)
    df.drop(columns=["emp_in"], inplace=True)


# --------------------------
# 6. CLEAN URBAN / RURAL
# --------------------------
if "urbanicity" in df.columns:
    df["urban_rural"] = df["urbanicity"].map({
        1: "Urban",
        2: "Rural"
    })
    df.drop(columns=["urbanicity"], inplace=True)


# --------------------------
# 7. CLEAN INCOME QUINTILE
# --------------------------
if "inc_q" in df.columns:
    df["income_quintile"] = df["inc_q"].replace({
        1: "Poorest 20%",
        2: "Second 20%",
        3: "Middle 20%",
        4: "Fourth 20%",
        5: "Richest 20%"
    })
    df.drop(columns=["inc_q"], inplace=True)


# --------------------------
# 8. CLEAN SIMPLE YES/NO VARIABLES
# --------------------------
yes_no_vars = [
    "account","account_fin","account_mob","dig_account",
    "anydigpayment","borrowed","saved","merchantpay_dig"
]

for col in yes_no_vars:
    if col in df.columns:
        df[col] = df[col].map({1: "Yes", 0: "No"})


# --------------------------
# 9. CLEAN MULTI-CATEGORY VARIABLES
# --------------------------

multi_maps = {
    "receive_wages": {
        1: "Into Account",
        2: "Cash Only",
        3: "Other Method",
        4: "No Wage",
        5: "Don't Know/Refused"
    },
    "receive_transfers": {
        1: "Into Account",
        2: "Cash Only",
        3: "Other Method",
        4: "No Transfer",
        5: "Don't Know/Refused"
    },
    "receive_pensions": {
        1: "Into Account",
        2: "Cash Only",
        3: "Other Method",
        4: "No Pension",
        5: "Don't Know/Refused"
    },
    "receive_agriculture": {
        1: "Into Account",
        2: "Cash Only",
        3: "Other Method",
        4: "No Agriculture Income",
        5: "Don't Know/Refused"
    },
    "pay_utilities": {
        1: "From Account",
        2: "Cash Only",
        3: "Other Method",
        4: "No Utility Payment",
        5: "Don't Know/Refused"
    },
    "domestic_remittances": {
        1: "Via Account",
        2: "Other Method",
        3: "No Remittances",
        4: "Don't Know/Refused"
    }
}

# Apply maps
for col, mapping in multi_maps.items():
    if col in df.columns:
        df[col] = df[col].map(mapping)


# --------------------------
# 10. EXPORT CLEAN FILE
# --------------------------

df.to_csv("findex_2025_cleaned.csv", index=False)
df.to_excel("findex_2025_cleaned.xlsx", index=False)

print("CLEANING COMPLETE — dataset ready for Tableau!")
df.head()
