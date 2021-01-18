import csv

def read_csv(csv_path):
    with open(csv_path, 'r', encoding='utf8', newline='') as f:
        csv_reader = csv.reader(f)
        return list(csv_reader)