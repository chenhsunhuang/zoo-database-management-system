"""Linked feeding records and negative inventory movements."""

from faker import Faker
from datetime import datetime, time
import random
import csv

fake = Faker("zh_TW")

A_IDS = [f"A{idx:03d}" for idx in range(1, 201)]
F_IDS = [f"F{idx:03d}" for idx in range(1, 21)]
E_IDS = [f"E{idx:03d}" for idx in range(1, 51)]

def gen_one_feeding(feeding_id: int) -> dict:
    a_id = random.choice(A_IDS)
    f_id = random.choice(F_IDS)
    fed_by = random.choice(E_IDS)

    feed_date = fake.date_between(start_date="-180d", end_date="today")

    feeding_amount_kg = round(random.uniform(1.0, 30.0), 2)

    return {
        "feeding_id": feeding_id,
        "a_id": a_id,
        "f_id": f_id,
        "feed_date": feed_date,
        "feeding_amount_kg": feeding_amount_kg,
        "fed_by": fed_by,
    }

def gen_feeding_records(n: int = 2000):
    return [gen_one_feeding(i) for i in range(1, n + 1)]

def export_feeding_to_csv(records, filename="feeding_records.csv"):
    fieldnames = ["feeding_id", "a_id", "f_id",
                  "feed_date", "feeding_amount_kg", "fed_by"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = r.copy()

            row["feed_date"] = row["feed_date"].strftime("%Y-%m-%d")
            writer.writerow(row)
    print(f"feeding_records CSV written: {filename} ({len(records)} rows)")

def gen_inventory_from_feeding(records):
    inventory = []
    stock_entry_id = 1
    locations = ["L001", "L002", "L003"]

    for r in records:
        feed_date = r["feed_date"]

        hour = random.randint(6, 20)
        minute = random.randint(0, 59)
        dt = datetime.combine(feed_date, time(hour=hour, minute=minute))

        inv_row = {
            "stock_entry_id": stock_entry_id,
            "f_id": r["f_id"],
            "location_id": random.choice(locations),
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "quantity_delta_kg": -round(r["feeding_amount_kg"], 2),
            "reason": "feeding",
            "feeding_id": r["feeding_id"],
        }
        inventory.append(inv_row)
        stock_entry_id += 1

    return inventory

def export_inventory_to_csv(inventory, filename="feeding_inventory.csv"):
    fieldnames = [
        "stock_entry_id",
        "f_id",
        "location_id",
        "datetime",
        "quantity_delta_kg",
        "reason",
        "feeding_id",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)
    print(f"feeding_inventory CSV written: {filename} ({len(inventory)} rows)")

if __name__ == "__main__":

    feeding_records = gen_feeding_records(2000)
    export_feeding_to_csv(feeding_records, "feeding_records.csv")

    inventory = gen_inventory_from_feeding(feeding_records)
    export_inventory_to_csv(inventory, "feeding_inventory.csv")
