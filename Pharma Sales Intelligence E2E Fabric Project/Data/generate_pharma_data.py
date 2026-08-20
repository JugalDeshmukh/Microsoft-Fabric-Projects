import numpy as np
import pandas as pd

# ==============================================================================
# 1. CREATE PHARMA LOOKUP FILE (pharma_product_lookup.csv)
# Matches structure: [LocationID, Borough, Zone, service_zone] -> [ProductID, TherapeuticArea, DrugName, MarketSegment]
# ==============================================================================
lookup_data = [
    {
        "ProductID": 1,
        "TherapeuticArea": "Cardiology",
        "DrugName": "LipidShield (Atorvastatin)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 2,
        "TherapeuticArea": "Cardiology",
        "DrugName": "VascuPress (Amlodipine)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 3,
        "TherapeuticArea": "Cardiology",
        "DrugName": "CardioBeta (Metoprolol)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 4,
        "TherapeuticArea": "Endocrinology",
        "DrugName": "GlucoReg (Metformin)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 5,
        "TherapeuticArea": "Endocrinology",
        "DrugName": "InsuPeak (Insulin Glargine)",
        "MarketSegment": "Prescription - Specialty",
    },
    {
        "ProductID": 6,
        "TherapeuticArea": "Endocrinology",
        "DrugName": "GlycoSGLT (Empagliflozin)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 7,
        "TherapeuticArea": "Oncology",
        "DrugName": "OncoTarget (Pembrolizumab)",
        "MarketSegment": "Biologics - Specialty",
    },
    {
        "ProductID": 8,
        "TherapeuticArea": "Oncology",
        "DrugName": "CytoBlock (Paclitaxel)",
        "MarketSegment": "Chemotherapy - Acute",
    },
    {
        "ProductID": 9,
        "TherapeuticArea": "Oncology",
        "DrugName": "ImmuShield (Nivolumab)",
        "MarketSegment": "Biologics - Specialty",
    },
    {
        "ProductID": 10,
        "TherapeuticArea": "Respiratory",
        "DrugName": "PulmoBreathe (Albuterol)",
        "MarketSegment": "Prescription - Acute",
    },
    {
        "ProductID": 11,
        "TherapeuticArea": "Respiratory",
        "DrugName": "AirClear (Fluticasone)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 12,
        "TherapeuticArea": "Neurology",
        "DrugName": "NeuroCalm (Gabapentin)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 13,
        "TherapeuticArea": "Neurology",
        "DrugName": "DopaRestore (Levodopa)",
        "MarketSegment": "Prescription - Chronic",
    },
    {
        "ProductID": 14,
        "TherapeuticArea": "Infectious Disease",
        "DrugName": "CiproMax (Ciprofloxacin)",
        "MarketSegment": "Antibiotic - Acute",
    },
    {
        "ProductID": 15,
        "TherapeuticArea": "Infectious Disease",
        "DrugName": "AmoxiGuard (Amoxicillin)",
        "MarketSegment": "Antibiotic - Acute",
    },
    {
        "ProductID": 16,
        "TherapeuticArea": "Immunology",
        "DrugName": "InflamMab (Adalimumab)",
        "MarketSegment": "Biologics - Specialty",
    },
    {
        "ProductID": 17,
        "TherapeuticArea": "Immunology",
        "DrugName": "DermaCalm (Dupilumab)",
        "MarketSegment": "Biologics - Specialty",
    },
    {
        "ProductID": 18,
        "TherapeuticArea": "Gastroenterology",
        "DrugName": "GastroRelief (Omeprazole)",
        "MarketSegment": "OTC / Prescription",
    },
]

df_lookup = pd.DataFrame(lookup_data)
df_lookup.to_csv("pharma_product_lookup.csv", index=False)
print("Successfully generated: pharma_product_lookup.csv")

# ==============================================================================
# 2. CREATE 5 MONTHLY PARQUET SALES FILES (Jan 2025 - May 2025)
# Generates files matching yellow_tripdata_2025-01.parquet to 05.parquet
# ==============================================================================
months = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05"]
rows_per_month = 150000  # Generates realistic enterprise volume

unit_prices = {
    1: 45.0,
    2: 30.0,
    3: 25.0,
    4: 20.0,
    5: 280.0,
    6: 180.0,
    7: 4500.0,
    8: 1200.0,
    9: 4800.0,
    10: 55.0,
    11: 95.0,
    12: 60.0,
    13: 110.0,
    14: 35.0,
    15: 18.0,
    16: 3200.0,
    17: 2900.0,
    18: 22.0,
}

for m in months:
    num_days = pd.Period(m).days_in_month
    start_ts = pd.to_datetime(f"{m}-01 00:00:00")
    end_ts = pd.to_datetime(f"{m}-{num_days} 23:59:59")

    # Generate synthetic transaction timestamps
    rand_seconds = np.random.randint(
        0, int((end_ts - start_ts).total_seconds()), size=rows_per_month
    )
    trx_dates = start_ts + pd.to_timedelta(rand_seconds, unit="s")

    # Product IDs corresponding to lookup table
    prod_ids = np.random.choice(
        list(unit_prices.keys()),
        size=rows_per_month,
        p=[
            0.12,
            0.10,
            0.08,
            0.15,
            0.05,
            0.06,
            0.02,
            0.02,
            0.01,
            0.10,
            0.06,
            0.06,
            0.03,
            0.05,
            0.05,
            0.015,
            0.015,
            0.01,
        ],
    )

    # Core pharmaceutical transaction fields
    units_sold = np.random.choice(
        [1, 2, 3, 5, 10, 30, 60, 90],
        size=rows_per_month,
        p=[0.40, 0.25, 0.15, 0.08, 0.05, 0.04, 0.02, 0.01],
    )

    # 1: Manufacturer Direct, 2: McKesson, 3: AmerisourceBergen, 6: Cardinal Health, 7: Specialty Direct
    distributor_ids = np.random.choice(
        [1, 2, 3, 6, 7], size=rows_per_month, p=[0.15, 0.35, 0.25, 0.20, 0.05]
    )

    # 1: Commercial Ins, 2: Medicare, 3: Medicaid, 4: Cash, 5: Government/VA
    payer_types = np.random.choice(
        [1, 2, 3, 4, 5], size=rows_per_month, p=[0.50, 0.25, 0.15, 0.05, 0.05]
    )

    # Financial calculations
    base_prices = np.array([unit_prices[pid] for pid in prod_ids])
    gross_amount = np.round(base_prices * units_sold, 2)
    rebate_pct = np.random.uniform(0.03, 0.22, size=rows_per_month)
    total_amount = np.round(gross_amount * (1 - rebate_pct), 2)

    df_sales = pd.DataFrame(
        {
            "trx_id": [
                f"TRX_{m.replace('-', '')}_{i:07d}"
                for i in range(rows_per_month)
            ],
            "VendorID": distributor_ids,
            "tpep_pickup_datetime": trx_dates,
            "ProductID": prod_ids,
            "payment_type": payer_types,
            "passenger_count": units_sold,
            "trip_distance": np.round(
                np.random.uniform(5.0, 500.0, size=rows_per_month), 1
            ),
            "total_amount": total_amount,
        }
    )

    file_name = f"pharma_sales_{m}.parquet"
    df_sales.to_parquet(file_name, engine="pyarrow", index=False)
    print(f"Successfully generated: {file_name}")