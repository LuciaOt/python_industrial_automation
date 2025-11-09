import os
import sys
import pandas as pd
from pymongo import MongoClient

print("Starting Data Transformation Process")

# -----------------------------
# MongoDB Connection Settings
# -----------------------------
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_DB = os.getenv("MONGO_DB", "welding_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "welding_data")

# Fail if any required credentials are missing
if not all([MONGO_HOST, MONGO_USER, MONGO_PASS]):
    print("MongoDB credentials missing! Check .env file.")
    sys.exit(1)

connection_string = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/"

# -----------------------------
# Connect to MongoDB
# -----------------------------
print(f"Connecting to MongoDB at {MONGO_HOST}...")

try:
    client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Test connection
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)

db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# -----------------------------
# Load CSV and transform
# -----------------------------
csv_path = "datasets/V1.1.csv"
try:
    df = pd.read_csv(csv_path)
    print(f"Loaded CSV with {len(df)} rows")
except Exception as e:
    print(f"Failed to read CSV: {e}")
    sys.exit(1)

df.columns = df.columns.str.strip()

# -----------------------------
# Insert data into MongoDB
# -----------------------------
try:
    records = df.to_dict(orient="records")
    if records:
        collection.insert_many(records)
        print(f"Inserted {len(records)} records into collection '{MONGO_COLLECTION}'")
    else:
        print("No records to insert")
except Exception as e:
    print(f"Failed to insert data into MongoDB: {e}")
    sys.exit(1)

print("Data Transformation Completed")
