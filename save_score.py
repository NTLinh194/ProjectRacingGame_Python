import csv

class csv_writer():

    def __init__(self, filename, delimiter=","):
        self.filename = filename
        self.delimiter = delimiter
    def write(self, data):
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(data)
