# populate.py
import csv
from models import db, Rooms, Devices, Faults


# CSV reader function
def read_csv(filename, model):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {k: v for k, v in row.items() if v}
            db.session.add(model(**data))


# Function populates data from CSV into Rooms, Devices and Faults
def populate_data():
    rooms_csv_path = r"C:\Users\jacob\PycharmProjects\Dissertation\data\rooms.csv"
    devices_csv_path = r"C:\Users\jacob\PycharmProjects\Dissertation\data\devices.csv"
    faults_csv_path = r"C:\Users\jacob\PycharmProjects\Dissertation\data\faults.csv"

    read_csv(rooms_csv_path, Rooms)
    read_csv(devices_csv_path, Devices)
    read_csv(faults_csv_path, Faults)
    db.session.commit()
