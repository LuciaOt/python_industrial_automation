from flask import Flask, jsonify, request
from pymongo import MongoClient
import sys
import os

app = Flask(__name__)

# MongoDB connection using env variables
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_DB = os.getenv("MONGO_DB", "welding_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "welding_data")

# Fail if any required credentials are missing
if not all([MONGO_HOST, MONGO_USER, MONGO_PASS]):
    print("MongoDB credentials missing! Check .env file.")
    sys.exit(1)


# Connection string with authentication (same as transform_data.py)
connection_string = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/"

# Connect to MongoDB
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


@app.route("/", methods=["GET"])
def home():
    """Home page with available endpoints"""
    return jsonify(
        {
            "message": "Welding Data API",
            "endpoints": {
                "/data": "GET all welding data (default limit: 100)",
                "/data?limit=10": "GET with custom limit",
                "/stats": "GET statistics about the data",
            },
        }
    )


@app.route("/data", methods=["GET"])
def get_welding_data():
    """Get welding data with optional limit parameter"""
    limit = request.args.get("limit", default=100, type=int)

    try:
        data = list(collection.find({}, {"_id": 0}).limit(limit))
        return jsonify({"count": len(data), "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics about the welding data"""
    try:
        total_count = collection.count_documents({})

        # Get some basic stats
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avg_power": {"$avg": "$power (W)"},
                    "avg_welding_speed": {"$avg": "$welding speed (m/min)"},
                    "total_with_cracks": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$eq": [
                                        "$cracking in the weld metal (yes/no)",
                                        "yes",
                                    ]
                                },
                                1,
                                0,
                            ]
                        }
                    },
                }
            }
        ]

        stats = list(collection.aggregate(pipeline))

        return jsonify(
            {"total_records": total_count, "statistics": stats[0] if stats else {}}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
