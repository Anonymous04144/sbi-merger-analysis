import numpy as np
import pandas as pd

# Set seed for reproducible results
np.random.seed(42)
TOTAL_ROWS = 4000

# Entities involved in the 2017 SBI consolidation
entities = [
    "State Bank of India (Parent)",
    "State Bank of Bikaner and Jaipur",
    "State Bank of Hyderabad",
    "State Bank of Mysore",
    "State Bank of Patiala",
    "State Bank of Travancore",
    "Bharatiya Mahila Bank"
]

circles = [
    "Mumbai Metro", "Delhi NCR", "Bengaluru", "Chennai", 
    "Hyderabad", "Kolkata", "Ahmedabad", "Jaipur", 
    "Chandigarh", "Thiruvananthapuram", "Bhopal", "Lucknow"
]

branch_tiers = ["Metro", "Urban", "Semi-Urban", "Rural"]
fiscal_years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

data = []

for i in range(1, TOTAL_ROWS + 1):
    branch_id = f"BR-{np.random.randint(1000, 9999)}"
    year = int(np.random.choice(fiscal_years))
    period = "Pre-Merger" if year <= 2017 else "Post-Merger"
    
    # Pre-merger associates vs Post-merger unified parent
    if period == "Pre-Merger":
        entity = np.random.choice(entities, p=[0.40, 0.12, 0.12, 0.10, 0.12, 0.10, 0.04])
        gross_npa = np.clip(np.random.normal(loc=9.8, scale=3.2), 2.1, 24.5)
        net_npa = gross_npa * np.random.uniform(0.50, 0.68)
        cost_to_income = np.clip(np.random.normal(loc=54.5, scale=4.5), 42.0, 68.0)
        roa = np.clip(np.random.normal(loc=0.35, scale=0.60), -1.8, 1.2)
        casa_ratio = np.clip(np.random.normal(loc=41.0, scale=4.0), 30.0, 52.0)
        car = np.clip(np.random.normal(loc=12.2, scale=1.1), 9.5, 14.5)
    else:
        entity = "State Bank of India (Consolidated)"
        gross_npa = np.clip(np.random.normal(loc=5.9, scale=1.9), 1.5, 12.5)
        net_npa = gross_npa * np.random.uniform(0.25, 0.45)
        cost_to_income = np.clip(np.random.normal(loc=47.2, scale=3.8), 37.0, 58.0)
        roa = np.clip(np.random.normal(loc=0.78, scale=0.35), 0.1, 1.6)
        casa_ratio = np.clip(np.random.normal(loc=45.5, scale=3.5), 35.0, 56.0)
        car = np.clip(np.random.normal(loc=14.1, scale=1.2), 11.5, 17.5)

    advances = round(float(np.random.uniform(80, 1500)), 2)
    deposits = round(advances * float(np.random.uniform(1.15, 1.45)), 2)
    
    data.append({
        "record_id": i,
        "branch_code": branch_id,
        "entity_name": entity,
        "circle_zone": np.random.choice(circles),
        "branch_tier": np.random.choice(branch_tiers, p=[0.25, 0.30, 0.25, 0.20]),
        "fiscal_year": year,
        "period_type": period,
        "merger_cutoff_date": "2017-04-01",
        "gross_npa_pct": f"{gross_npa:.2f}%",
        "net_npa_pct": f"{net_npa:.2f}%",
        "cost_to_income_pct": f"{cost_to_income:.2f}%",
        "roa_pct": f"{roa:.2f}%",
        "casa_ratio_pct": f"{casa_ratio:.2f}%",
        "car_crar_pct": f"{car:.2f}%",
        "advances_inr_cr": f"{advances:,.2f}",
        "deposits_inr_cr": f"{deposits:,.2f}"
    })

df = pd.DataFrame(data)

# Inject dirty data artifacts for cleaning
df.loc[df.sample(frac=0.08, random_state=42).index, "entity_name"] += "   "
df.loc[df.sample(frac=0.03, random_state=42).index, "cost_to_income_pct"] = np.nan
df.loc[df.sample(frac=0.02, random_state=42).index, "net_npa_pct"] = np.nan
df.loc[df.sample(frac=0.30, random_state=42).index, "merger_cutoff_date"] = "01/04/2017"

# Save CSV file
output_filename = "sbi_merger_raw_4000.csv"
df.to_csv(output_filename, index=False)
print(f"File successfully created: {output_filename}")
print(f"Total Rows: {len(df)} | Columns: {len(df.columns)}")