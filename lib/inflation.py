"""
Core personal-inflation calculation logic.

Formula:
    personal_rate = sum( (spend_category / total_spend) * cpi_pct_change_category )

cpi_pct_change_category = (current_index - base_index) / base_index * 100
"""
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cpi_india.json")

PERIOD_TO_MONTHS = {
    "3 months": 3,
    "6 months": 6,
    "1 year": 12,
    "3 years": 36,
}

CATEGORY_ORDER = [
    "food_beverages",
    "housing",
    "fuel_light",
    "clothing",
    "transport",
    "healthcare",
    "education",
    "misc",
]


def load_cpi_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def pct_change(base_index, current_index):
    if base_index == 0:
        return 0.0
    return (current_index - base_index) / base_index * 100.0


def get_category_series(data, category_key, area):
    field = "index_urban" if area == "Urban" else "index_rural"
    return data["categories"][category_key][field]


def get_headline_series(data, area):
    field = "index_urban" if area == "Urban" else "index_rural"
    return data["headline"][field]


def compute_personal_inflation(spend: dict, period: str, area: str = "Urban"):
    """
    spend: dict of category_key -> monthly spend in INR
    period: one of '3 months', '6 months', '1 year', '3 years'
    area: 'Urban' or 'Rural'
    """
    data = load_cpi_data()
    months_back = PERIOD_TO_MONTHS.get(period, 12)

    total_spend = sum(v for v in spend.values() if v and v > 0)
    if total_spend <= 0:
        return {
            "personal_rate": 0.0,
            "national_rate": 0.0,
            "contributions": [],
            "total_spend": 0.0,
        }

    contributions = []
    personal_rate = 0.0

    for cat_key in CATEGORY_ORDER:
        cat_spend = spend.get(cat_key, 0) or 0
        if cat_spend <= 0:
            continue
        series = get_category_series(data, cat_key, area)
        n = len(series)
        idx_start = max(0, n - 1 - months_back)
        base_index = series[idx_start]
        current_index = series[-1]
        cat_pct_change = pct_change(base_index, current_index)

        weight = cat_spend / total_spend
        weighted_contribution = weight * cat_pct_change
        personal_rate += weighted_contribution

        contributions.append({
            "category": cat_key,
            "label": data["categories"][cat_key]["label"],
            "spend": cat_spend,
            "weight": round(weight * 100, 2),
            "cpi_pct_change": round(cat_pct_change, 2),
            "contribution": round(weighted_contribution, 3),
        })

    headline_series = get_headline_series(data, area)
    n = len(headline_series)
    idx_start = max(0, n - 1 - months_back)
    national_rate = pct_change(headline_series[idx_start], headline_series[-1])

    contributions.sort(key=lambda c: abs(c["contribution"]), reverse=True)

    return {
        "personal_rate": round(personal_rate, 2),
        "national_rate": round(national_rate, 2),
        "contributions": contributions,
        "total_spend": total_spend,
    }