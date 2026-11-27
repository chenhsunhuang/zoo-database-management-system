"""Generate the seven synthetic CSV files in a dedicated directory."""
import argparse
from pathlib import Path
import subprocess
import sys

SCRIPTS = ["generate_animals.py", "generate_employees.py", "generate_tasks.py",
           "generate_shifts.py", "generate_feeding_inventory.py", "generate_health_records.py"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/generated"))
    args = parser.parse_args()
    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for script in SCRIPTS:
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / script)],
                       cwd=destination, check=True)
