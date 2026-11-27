"""Animal IDs, species, sex and life-status generation."""

from faker import Faker
from faker.providers import BaseProvider
from datetime import date, timedelta
import random
import csv

class ZooAnimalProvider(BaseProvider):
    species_list = [
        "African Elephant", "Lion", "Tiger", "Giraffe",
        "Panda", "Koala", "Hippopotamus", "Zebra",
        "Brown Bear", "Penguin"
    ]

    def animal_species(self):
        return self.random_element(self.species_list)

    def animal_sex(self):
        return self.random_element(["M", "F"])

    def animal_life_status(self):
        return self.random_element(
            ["Alive"] * 8 + ["Transferred"] * 1 + ["Deceased"] * 1
        )

fake = Faker("zh_TW")
fake.add_provider(ZooAnimalProvider)

def random_birth_and_arrival():
    today = date.today()
    birth = today - timedelta(days=random.randint(365, 365 * 30))
    min_arrival = birth + timedelta(days=365)
    if min_arrival > today:
        min_arrival = birth + timedelta(days=100)
    arrival_delta_days = random.randint(0, (today - min_arrival).days)
    arrival = min_arrival + timedelta(days=arrival_delta_days)
    return birth, arrival

def format_animal_id(idx: int) -> str:

    return f"A{idx:03d}"

def gen_one_animal(idx: int):

    return {
        "a_id": format_animal_id(idx),
        "species": fake.animal_species(),
        "sex": fake.animal_sex(),
        "life_status": fake.animal_life_status()
    }

def gen_animals(n=50):
    return [gen_one_animal(i) for i in range(1, n + 1)]

def export_animals_to_csv(animals, filename="animals.csv"):
    fieldnames = ["a_id", "species", "sex", "life_status"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(animals)
    print(f"CSV written to {filename} with {len(animals)} rows.")

if __name__ == "__main__":
    animals = gen_animals(200)
    export_animals_to_csv(animals, "animals.csv")
