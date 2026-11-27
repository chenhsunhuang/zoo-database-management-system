"""Employee shifts, including overnight shifts."""

from faker import Faker
from datetime import datetime, date, time, timedelta
import random
import csv

fake = Faker("zh_TW")

E_IDS = [f"E{idx:03d}" for idx in range(1, 51)]
T_IDS = [f"T{idx:03d}" for idx in range(1, 9)]

def gen_one_shift(shift_id: int) -> dict:
    e_id = random.choice(E_IDS)
    t_id = random.choice(T_IDS)

    shift_date = fake.date_between(start_date="-90d", end_date="today")

    start_hour, end_hour = random.choice([
        (8, 16),
        (14, 22),
        (22, 6),
    ])

    start_dt = datetime.combine(shift_date, time(hour=start_hour))

    if end_hour > start_hour:
        end_dt = datetime.combine(shift_date, time(hour=end_hour))
    else:
        end_dt = datetime.combine(shift_date + timedelta(days=1),
                                  time(hour=end_hour))

    return {
        "shift_id": f"S{shift_id:04d}",
        "e_id": e_id,
        "t_id": t_id,
        "shift_start": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "shift_end":   end_dt.strftime("%Y-%m-%d %H:%M:%S"),
    }

def gen_shifts(n: int = 500):
    return [gen_one_shift(i) for i in range(1, n + 1)]

def export_shifts_to_csv(shifts, filename: str = "employee_shift.csv"):
    fieldnames = ["shift_id", "e_id", "t_id", "shift_start", "shift_end"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(shifts)
    print(f"CSV written to {filename} with {len(shifts)} rows.")

if __name__ == "__main__":
    shifts = gen_shifts(500)
    export_shifts_to_csv(shifts)
