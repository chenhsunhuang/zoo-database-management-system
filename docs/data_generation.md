# Synthetic Data Generation

Python and Faker generate source tables for the course database. Run `python data_generation/run_all.py` from the repository root. Output is written to `data/generated/`, or another directory specified by `--output`.

| Script | CSV output | Default run rows |
|---|---|---:|
| generate_animals.py | animals.csv | 200 |
| generate_employees.py | employees.csv | 50 |
| generate_tasks.py | task.csv | 8 |
| generate_shifts.py | employee_shift.csv | 500 |
| generate_feeding_inventory.py | feeding_records.csv; feeding_inventory.csv | 2,000 each |
| generate_health_records.py | animal_state_record.csv | 15,000 |

## Generation logic

Animal and employee identifiers are formatted consistently so other generators can reference them. Employee attributes use localized Faker providers. Task names are selected from a task vocabulary. Shift start dates are drawn from the previous 90 days; overnight shifts end on the next calendar day.

Feeding records reference the defined animal, feed, and employee identifier ranges, use dates within the preceding 180 days, and sample amounts from 1 to 30 kg. Each feeding event produces one inventory movement with a matching feed identifier, feeding identifier, and negative quantity. These source movements describe consumption, not opening stock or purchases.

Health records read the generated animal master file. Each animal receives a baseline weight sampled from a species-specific range. Individual observations use a normal distribution centered at that animal's baseline with standard deviation equal to 5% of its baseline. Observations are bounded below at 1 kg and rounded to one decimal place. The health state is sampled with probability 0.6 for state 1 and equal probability for the remaining five states. This is a simulation specification, not a veterinary model.

The generators preserve the course sampling design. They produce randomized CSVs for seven tables; final system initialization also requires master/reference tables, diet rules, qualifications, role and assignment fields, and opening inventory. The final populated database is documented in [database_summary.csv](../results/database_summary.csv). No generated employee names or contact details are included in this repository.
