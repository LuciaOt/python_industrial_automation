from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection using env variables
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb-container")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "welding_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "welding_data")

client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


@app.route("/data", methods=["GET"])
def get_welding_data():
    data = list(collection.find({}, {"_id": 0}).limit(10))  # limit to first 10 rows
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
