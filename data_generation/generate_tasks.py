"""Synthetic task reference records."""

from faker import Faker
from faker.providers import BaseProvider
import csv

class TaskProvider(BaseProvider):
    task_names = [
        "餵食紀錄",
        "體重測量",
        "健康檢查",
        "籠舍清潔",
        "環境消毒",
        "行為觀察",
        "用藥紀錄",
        "特殊訓練"
    ]

    def task_name(self):
        return self.random_element(self.task_names)

fake = Faker("zh_TW")
fake.add_provider(TaskProvider)

def gen_one_task(t_id: int) -> dict:
    return {
        "t_id": f"T{t_id:03d}",
        "t_name": fake.task_name()
    }

def gen_tasks(n: int = 8):
    return [gen_one_task(i) for i in range(1, n + 1)]

def export_tasks_to_csv(tasks, filename: str = "task.csv"):
    fieldnames = ["t_id", "t_name"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)
    print(f"CSV written to {filename} with {len(tasks)} rows.")

if __name__ == "__main__":
    tasks = gen_tasks(8)
    export_tasks_to_csv(tasks)
