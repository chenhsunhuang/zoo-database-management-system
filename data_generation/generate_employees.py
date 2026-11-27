"""Synthetic employee attributes and identifiers."""

from faker import Faker
from faker.providers import BaseProvider
from datetime import date, timedelta
import random
import csv

class EmployeeProvider(BaseProvider):
    def employee_sex(self):

        return self.random_element(["M", "F","Unknown"])

    def employee_status(self):

        return self.random_element(["active", "inactive","leave"])

fake = Faker("zh_TW")
fake.add_provider(EmployeeProvider)

def format_employee_id(idx: int) -> str:

    return f"E{idx:03d}"

def gen_one_employee(idx: int) -> dict:
    sex = fake.employee_sex()

    if sex == "M":
        name = fake.name_male()
    else:
        name = fake.name_female()

    start_time = fake.date_between(start_date="-5y", end_date="today")

    return {
        "e_id": format_employee_id(idx),
        "e_name": name,
        "sex": sex,
        "phone": fake.phone_number(),
        "start_time": start_time,
        "status": fake.employee_status()
    }

def gen_employees(n: int = 100):
    return [gen_one_employee(i) for i in range(1, n + 1)]

def export_employees_to_csv(employees, filename: str = "employees.csv"):
    fieldnames = ["e_id", "e_name", "sex", "phone", "start_time", "status"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)
    print(f"CSV written to {filename} with {len(employees)} rows.")

if __name__ == "__main__":
    employees = gen_employees(50)
    export_employees_to_csv(employees)
