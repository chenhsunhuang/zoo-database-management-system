"""Species-specific baseline weights and simulated health observations."""

from faker import Faker
from datetime import datetime
import random
import csv
import pandas as pd

fake = Faker("zh_TW")

animals_df = pd.read_csv("animals.csv")

species_weight_ranges = {
    "African Elephant": (2500, 6000),
    "Lion":             (120, 250),
    "Tiger":            (100, 300),
    "Giraffe":          (600, 1500),
    "Panda":            (70, 150),
    "Koala":            (5, 15),
    "Hippopotamus":     (1400, 4500),
    "Zebra":            (200, 450),
    "Brown Bear":       (100, 600),
    "Penguin":          (15, 40),
}

def choose_base_weight(species: str) -> float:

    mn, mx = species_weight_ranges.get(species, (30, 300))
    return random.uniform(mn, mx)

animals_df["base_weight"] = animals_df["species"].apply(choose_base_weight)

base_weights = dict(zip(animals_df["a_id"], animals_df["base_weight"]))

E_IDS = [f"E{idx:03d}" for idx in range(1, 51)]

def pick_state_id() -> int:

    r = random.random()
    if r < 0.6:
        return 1
    else:
        return random.choice([2, 3, 4, 5, 6])

def gen_one_state_record(record_id: int) -> dict:

    a_id = random.choice(list(base_weights.keys()))
    base_w = base_weights[a_id]

    dt = fake.date_time_between(start_date="-365d", end_date="now")

    weight = random.gauss(mu=base_w, sigma=base_w * 0.05)
    weight = max(1.0, weight)
    weight = round(weight, 1)

    state_id = pick_state_id()
    recorded_by = random.choice(E_IDS)

    return {
        "record_id": record_id,
        "a_id": a_id,
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "weight": weight,
        "state_id": state_id,
        "recorded_by": recorded_by,
    }

def gen_state_records(n: int = 15000):
    return [gen_one_state_record(i) for i in range(1, n + 1)]

def export_state_records_to_csv(records, filename: str = "animal_state_record.csv"):
    fieldnames = ["record_id", "a_id", "datetime",
                  "weight", "state_id", "recorded_by"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"CSV written to {filename} with {len(records)} rows.")

if __name__ == "__main__":
    records = gen_state_records(15000)
    export_state_records_to_csv(records)
