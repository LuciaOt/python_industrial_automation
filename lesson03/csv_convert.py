# -------------------------------
# Binary parsing in python
# -------------------------------
import csv
import struct

FILE_TO_READ = "datasets/raw_tracking/raw-teststream-20250925-151535"
# do not forget to create the folder "temp" if it does not exist
CSV_TO_WRITE = "temp/raw-teststream-20250925-151535.csv"
PANDAS_CSV = "temp/raw-teststream-20250925-151535_pandas.csv"

# --- First part: Write parsed binary data to CSV using csv.writer ---
with open(FILE_TO_READ, "rb") as f:
    with open(CSV_TO_WRITE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write CSV header
        writer.writerow(
            [
                "frame_id",
                "timestamp",
                "rb_index",
                "enabled",
                "tracked",
                "valid",
                "mean_error",
                "pos_x",
                "pos_y",
                "pos_z",
                "orientation_x",
                "orientation_y",
                "orientation_z",
                "orientation_w",
            ]
        )
        while True:
            size = struct.calcsize("<iQHHffffffff")  # 48 bytes per record
            data = f.read(size)
            if data:
                # Unpack binary data according to format
                unpacked_data = struct.unpack("<iQHHffffffff", data)
                # Write unpacked and processed data to CSV
                writer.writerow(
                    [
                        unpacked_data[0],  # frame_id
                        unpacked_data[1],  # timestamp
                        unpacked_data[2],  # rb_index
                        int(bool(unpacked_data[3] & 0x01)),  # enabled flag
                        int(bool(unpacked_data[3] & 0x02)),  # tracked flag
                        int(bool(unpacked_data[3] & 0x04)),  # valid flag
                        unpacked_data[4],  # mean_error
                        unpacked_data[5],  # pos_x
                        unpacked_data[6],  # pos_y
                        unpacked_data[7],  # pos_z
                        unpacked_data[8],  # orientation_x
                        unpacked_data[9],  # orientation_y
                        unpacked_data[10],  # orientation_z
                        unpacked_data[11],  # orientation_w
                    ]
                )
            else:
                break

import pandas as pd

# --- Second part: Write parsed binary data to CSV using pandas.DataFrame ---
with open(FILE_TO_READ, "rb") as f:
    index = 0
    while True:
        size = struct.calcsize("<iQHHffffffff")  # 48 bytes per record
        data = f.read(size)
        if data:
            # Unpack binary data according to format
            unpacked_data = struct.unpack("<iQHHffffffff", data)
            unpacked_data = list(unpacked_data)
            # Add boolean flags as separate columns
            unpacked_data.append(int(bool(unpacked_data[3] & 0x01)))  # enabled_bool
            unpacked_data.append(int(bool(unpacked_data[3] & 0x02)))  # tracked_bool
            unpacked_data.append(int(bool(unpacked_data[3] & 0x04)))  # valid_bool
            unpacked_data.pop(3)  # remove original flags field
            # Create DataFrame for this record
            df = pd.DataFrame(
                [unpacked_data],
                columns=[
                    "frame_id",
                    "timestamp",
                    "rb_index",
                    "mean_error",
                    "pos_x",
                    "pos_y",
                    "pos_z",
                    "orientation_x",
                    "orientation_y",
                    "orientation_z",
                    "orientation_w",
                    "enabled_bool",
                    "tracked_bool",
                    "valid_bool",
                ],
            )
            # Write or append to CSV
            if index == 0:
                df.to_csv(PANDAS_CSV, mode="w", header=True, index=False)
            else:
                df.to_csv(PANDAS_CSV, mode="a", header=False, index=False)
            index += 1
        else:
            break


test = pd.read_csv(
    PANDAS_CSV,
)
print("OK")
