"""
Run this once to create data/cpi_india.json — a static fallback dataset
matching MOSPI's CPI structure (base year 2012=100), 36 months of history
across all 8 official categories, for both Urban and Rural India.
"""
import json
import random
from datetime import date

random.seed(42)

categories = {
    "food_beverages": {"label": "Food & beverages", "start": 172.0, "drift": 0.55, "vol": 0.9},
    "housing": {"label": "Housing", "start": 168.0, "drift": 0.35, "vol": 0.3},
    "fuel_light": {"label": "Fuel & light", "start": 175.0, "drift": 0.30, "vol": 1.4},
    "clothing": {"label": "Clothing", "start": 158.0, "drift": 0.28, "vol": 0.3},
    "transport": {"label": "Transport", "start": 165.0, "drift": 0.32, "vol": 0.8},
    "healthcare": {"label": "Healthcare", "start": 170.0, "drift": 0.40, "vol": 0.4},
    "education": {"label": "Education", "start": 173.0, "drift": 0.42, "vol": 0.2},
    "misc": {"label": "Miscellaneous goods & services", "start": 166.0, "drift": 0.33, "vol": 0.5},
}

months = 36
today = date(2026, 6, 1)
m, y = today.month, today.year
month_dates = []
for i in range(months):
    mm, yy = m - i, y
    while mm <= 0:
        mm += 12
        yy -= 1
    month_dates.append((yy, mm))
month_dates.reverse()

data = {"base_year": "2012=100", "months": [], "categories": {}}

for key, cfg in categories.items():
    vals = []
    v = cfg["start"] - cfg["drift"] * months
    for i in range(months):
        v += cfg["drift"] + random.uniform(-cfg["vol"], cfg["vol"])
        vals.append(round(v, 2))
    if key == "food_beverages":
        vals[10] += 3.5
        vals[11] += 2.0
    if key == "fuel_light":
        vals[6] += 5.0
        vals[20] += 4.0
    data["categories"][key] = {
        "label": cfg["label"],
        "index_urban": vals,
        "index_rural": [round(x - random.uniform(0.5, 2.5), 2) for x in vals],
    }

data["months"] = [f"{yy}-{mm:02d}" for yy, mm in month_dates]

weights = {
    "food_beverages": 0.39, "housing": 0.10, "fuel_light": 0.08,
    "clothing": 0.065, "transport": 0.084, "healthcare": 0.059,
    "education": 0.042, "misc": 0.18,
}
headline_urban, headline_rural = [], []
for i in range(months):
    hu = sum(data["categories"][k]["index_urban"][i] * w for k, w in weights.items())
    hr = sum(data["categories"][k]["index_rural"][i] * w for k, w in weights.items())
    headline_urban.append(round(hu, 2))
    headline_rural.append(round(hr, 2))
data["headline"] = {"index_urban": headline_urban, "index_rural": headline_rural}
data["weights"] = weights

import os
out_path = os.path.join(os.path.dirname(__file__), "cpi_india.json")
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Created {out_path} with {len(data['months'])} months of data.")