# csv_ops.py - read and write CSV data
import csv
import os

def check_scratch(dir_name):
    """Create the full tree to the specified path, if it doesn't already exist

    dir_name: folder path (absolute or relative)
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def import_csv(filename):
    """Return a list of dicts containing the data read from the specified CSV files
    Dict keys are the CSV headers

    filename: path to the CSV file
    """
    data = []
    with open(filename) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append({a: row[a].strip() for a in row})

    return data

def export_csv(headers, data, filename):
    """Write a new CSV with updated data to be passed back to DMT

    headers: list of the headers to write as the first line of the CSV file
    data: data to fill in the body, composed as a list of dicts
    filename: name of the new CSV file to write
    """
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file,
                                    extrasaction='ignore',
                                    fieldnames=headers,
                                    lineterminator='\n',
                                    quoting=csv.QUOTE_NONNUMERIC)

        csv_writer.writeheader()
        csv_writer.writerows(data)
