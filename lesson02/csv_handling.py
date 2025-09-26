# -------------------------------
# CSV Handling in Python
# -------------------------------
import csv

CSV_TO_READ = "datasets/robot_imu_comparison/R1.csv"

# read CSV file and calculate average of the second column
with open(CSV_TO_READ, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    total = 0.0
    count = 0
    for row in reader:
        if len(row) > 1:  # check if there is a second column
            try:
                value = float(row[1])
                total += value
                count += 1
            except ValueError:
                continue
    if count > 0:
        average = total / count
        print(f"Average of second column: {average:.2f}")
