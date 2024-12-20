
import csv
import random

with open('dati.csv', 'w', newline='') as csvfile:
    fieldnames = ['Diamtrs', 'Laiks3', 'Laiks2', 'Laiks1']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(10000):
        writer.writerow({
            'Diamtrs': round(random.uniform(0, 3), 3),
            'Laiks3': round(random.uniform(0, 60), 2),
            'Laiks2': round(random.uniform(0, 60), 2),
            'Laiks1': round(random.uniform(0, 60), 2)
        })