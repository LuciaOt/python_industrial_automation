from flask import Flask, request, render_template_string
from pymongo import MongoClient
import sys, os
import pandas as pd

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

# Connection string
connection_string = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/"

# Connect to MongoDB
try:
    client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)

db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


@app.route("/", methods=["GET"])
def home():
    return """
    <h2>Welding Data API</h2>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/data">/data</a> - View welding data in a table (default limit: 100)</li>
        <li>/data?limit=10 - View first 10 records</li>
    </ul>
    """


@app.route("/data", methods=["GET"])
def get_welding_data():
    limit = request.args.get("limit", default=100, type=int)
    try:
        # Fetch data from MongoDB
        data = list(collection.find({}, {"_id": 0}).limit(limit))
        if not data:
            return "<p>No data found.</p>"

        # Convert to pandas DataFrame for easy HTML table rendering
        df = pd.DataFrame(data)
        html_table = df.to_html(classes="table table-striped", index=False)

        # Render simple HTML page with table
        html = f"""
        <html>
            <head>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            </head>
            <body style="margin:20px;">
                <h2>Welding Data (showing {len(data)} records)</h2>
                {html_table}
            </body>
        </html>
        """
        return render_template_string(html)
    except Exception as e:
        return f"<p>Error: {str(e)}</p>", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
