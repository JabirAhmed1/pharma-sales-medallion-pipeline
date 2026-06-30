import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/raw"
NUM_PRODUCTS = 20
NUM_PROVIDERS = 200
NUM_PRESCRIPTIONS = 10000


# -----------------------------
# Helper functions
# -----------------------------
def random_date(start_date: str, end_date: str) -> datetime:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


# -----------------------------
# Create output folder
# -----------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Regions
# -----------------------------
regions = pd.DataFrame({
    "region_id": ["REG001", "REG002", "REG003", "REG004"],
    "region_name": ["Northeast", "Southeast", "Midwest", "West"],
    "sales_director": ["Ava Thompson", "Marcus Lee", "Priya Shah", "Daniel Kim"]
})


# -----------------------------
# Products
# -----------------------------
therapeutic_areas = ["Cardiology", "Diabetes", "Neurology", "Oncology", "Immunology"]

product_names = [
    "CardioMax", "GlycoCare", "NeuroPlus", "OncoRelief", "Immunex",
    "HeartSure", "GlucosePro", "NeuroCalm", "TumorClear", "ImmuneGuard",
    "VascuEase", "InsuBalance", "MigraFree", "CellShield", "AllerBlock",
    "PulseRX", "SugarStat", "BrainWell", "OncoNova", "BioDefend"
]

products = pd.DataFrame({
    "product_id": [f"PROD{i:03d}" for i in range(1, NUM_PRODUCTS + 1)],
    "product_name": product_names,
    "therapeutic_area": [random.choice(therapeutic_areas) for _ in range(NUM_PRODUCTS)],
    "launch_year": [random.randint(2010, 2025) for _ in range(NUM_PRODUCTS)],
    "list_price": np.round(np.random.uniform(75, 750, NUM_PRODUCTS), 2)
})


# -----------------------------
# Providers
# -----------------------------
first_names = [
    "Sarah", "Michael", "Priya", "David", "Emily", "Daniel", "Aisha", "James",
    "Sophia", "Omar", "Linda", "Kevin", "Rachel", "Anthony", "Nina", "Carlos"
]

last_names = [
    "Patel", "Chen", "Smith", "Johnson", "Garcia", "Ahmed", "Brown", "Kim",
    "Lee", "Davis", "Wilson", "Martinez", "Taylor", "Anderson", "Thomas", "Moore"
]

specialties = [
    "Cardiology", "Endocrinology", "Neurology", "Oncology",
    "Immunology", "Primary Care", "Internal Medicine"
]

providers = pd.DataFrame({
    "provider_id": [f"PRV{i:03d}" for i in range(1, NUM_PROVIDERS + 1)],
    "provider_name": [
        f"Dr. {random.choice(first_names)} {random.choice(last_names)}"
        for _ in range(NUM_PROVIDERS)
    ],
    "specialty": [random.choice(specialties) for _ in range(NUM_PROVIDERS)],
    "years_practicing": [random.randint(1, 35) for _ in range(NUM_PROVIDERS)]
})


# -----------------------------
# Prescriptions
# -----------------------------
payer_types = ["Commercial", "Medicare", "Medicaid", "Cash"]
age_groups = ["18-34", "35-49", "50-64", "65+"]

prescription_rows = []

for i in range(1, NUM_PRESCRIPTIONS + 1):
    product = products.sample(1).iloc[0]
    quantity = random.randint(1, 6)

    gross_sales = round(product["list_price"] * quantity, 2)
    discount_rate = np.random.uniform(0.02, 0.25)
    discount = round(gross_sales * discount_rate, 2)
    net_sales = round(gross_sales - discount, 2)

    prescription_rows.append({
        "prescription_id": f"RX{i:06d}",
        "prescription_date": random_date("2024-01-01", "2025-12-31").strftime("%Y-%m-%d"),
        "provider_id": random.choice(providers["provider_id"].tolist()),
        "product_id": product["product_id"],
        "region_id": random.choice(regions["region_id"].tolist()),
        "patient_age_group": random.choice(age_groups),
        "payer_type": random.choice(payer_types),
        "quantity": quantity,
        "gross_sales": gross_sales,
        "discount": discount,
        "net_sales": net_sales
    })

prescriptions = pd.DataFrame(prescription_rows)


# -----------------------------
# Save files
# -----------------------------
regions.to_csv(f"{OUTPUT_DIR}/raw_regions.csv", index=False)
products.to_csv(f"{OUTPUT_DIR}/raw_products.csv", index=False)
providers.to_csv(f"{OUTPUT_DIR}/raw_providers.csv", index=False)
prescriptions.to_csv(f"{OUTPUT_DIR}/raw_prescriptions.csv", index=False)


# -----------------------------
# Summary output
# -----------------------------
print("Generating Pharma Sales Dataset...\n")
print(f"✓ Regions created: {len(regions)}")
print(f"✓ Products created: {len(products)}")
print(f"✓ Providers created: {len(providers)}")
print(f"✓ Prescriptions created: {len(prescriptions)}")
print(f"\nFiles written to: {OUTPUT_DIR}")
print("\nDataset generation complete.")

