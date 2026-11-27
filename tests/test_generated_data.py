import csv
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]

class GeneratedDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.folder = Path(cls.temp.name)
        subprocess.run([sys.executable, str(ROOT / 'data_generation/run_all.py'),
                        '--output', str(cls.folder)], check=True, capture_output=True)
        cls.data = {}
        for file in cls.folder.glob('*.csv'):
            with file.open(encoding='utf-8', newline='') as f:
                cls.data[file.stem] = list(csv.DictReader(f))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_counts(self):
        expected = {'animals': 200, 'employees': 50, 'task': 8, 'employee_shift': 500,
                    'feeding_records': 2000, 'feeding_inventory': 2000, 'animal_state_record': 15000}
        self.assertEqual({k: len(v) for k, v in self.data.items()}, expected)

    def test_inventory_links(self):
        feeding = {r['feeding_id']: r for r in self.data['feeding_records']}
        self.assertEqual(len(feeding), 2000)
        self.assertEqual(len({r['feeding_id'] for r in self.data['feeding_inventory']}), 2000)
        for row in self.data['feeding_inventory']:
            event = feeding[row['feeding_id']]
            self.assertEqual(row['f_id'], event['f_id'])
            self.assertEqual(Decimal(row['quantity_delta_kg']), -Decimal(event['feeding_amount_kg']))

    def test_health_links(self):
        animals = {r['a_id'] for r in self.data['animals']}
        employees = {r['e_id'] for r in self.data['employees']}
        for row in self.data['animal_state_record']:
            self.assertIn(row['a_id'], animals)
            self.assertIn(row['recorded_by'], employees)
            self.assertIn(int(row['state_id']), range(1, 7))
            self.assertGreaterEqual(float(row['weight']), 1)

    def test_shifts(self):
        employees = {r['e_id'] for r in self.data['employees']}
        tasks = {r['t_id'] for r in self.data['task']}
        for row in self.data['employee_shift']:
            self.assertIn(row['e_id'], employees)
            self.assertIn(row['t_id'], tasks)
            self.assertEqual((datetime.fromisoformat(row['shift_end']) -
                              datetime.fromisoformat(row['shift_start'])).total_seconds(), 8 * 3600)

if __name__ == '__main__':
    unittest.main()
