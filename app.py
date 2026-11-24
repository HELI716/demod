import os

from flask import Flask
from pymongo import MongoClient, ReturnDocument

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["demod"]
counters = db["counters"]


@app.route("/")
def hello():
    result = counters.find_one_and_update(
        {"_id": "visits"},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return f"Hello from Docker! Visits: {result['count']}\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
