import json
import os
import csv
from glob import glob

raw_files = glob("data/raw/*.json")
output_file = "data/clean_rates.csv"

rows = []
for file in raw_files:
    with open(file) as f:
        data = json.load(f)
    date = data["time_last_update_utc"]
    for currency, rate in data["conversion_rates"].items():
        rows.append([date, currency, rate])

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Currency", "Rate"])
    writer.writerows(rows)

print(f"Transformed {len(raw_files)} files into {output_file}")