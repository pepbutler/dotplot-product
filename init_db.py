import sqlite3
import csv

patient_scan = dict()


def main() -> None:
    connection = sqlite3.connect("database.db")
    with open("files/schema.sql") as f:
        connection.executescript(f.read())
    with open("files/Patients.csv", "r") as patient_fp:
        reader = csv.reader(patient_fp)
        next(reader)
        for row in reader:
            print(row)
            id, name, age, height, weight, history, scan_ids = row
            id = int(id)
            age = int(age)
            height = int(height)
            weight = int(weight)
            history = history == "Yes"
            for sid in scan_ids.split():
                patient_scan[int(sid)] = id
            cur = connection.cursor()
            cur.execute(
                "INSERT INTO patient VALUES (?, ?, ?, ?, ?, ?)",
                (id, name, age, height, weight, history),
            )
    with open("files/US_scans.csv", "r") as scans_fp:
        reader = csv.reader(scans_fp)
        next(reader)
        for row in reader:
            id, coords, date, diagnosis = row
            id = int(id)
            is_malignant = diagnosis == "Malignant"
            cur = connection.cursor()
            cur.execute(
                "INSERT INTO scan VALUES (?, ?, ?, ?, ?)",
                (id, coords, date, is_malignant, patient_scan.get(id) or "-1"),
            )
            connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
