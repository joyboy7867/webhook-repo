# File: app.py
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS
import os
import pytz
load_dotenv() 
app = Flask(__name__)
CORS(app)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["github_events"]
collection = db["events"]

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    data = request.json

    if event_type == "push":
        author = data.get("pusher", {}).get("name", "Unknown")
        to_branch = data.get("ref", "").split("/")[-1]
        timestamp = data.get("head_commit", {}).get("timestamp", datetime.utcnow().isoformat())

        record = {
            "author": author,
            "action_type": "push",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
        collection.insert_one(record)

    elif event_type == "pull_request":
        action = data.get("action")
        pr = data.get("pull_request", {})
        author = pr.get("user", {}).get("login", "Unknown")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")
        timestamp = pr.get("created_at", datetime.utcnow().isoformat())

        # Save if it's either opened or merged
        if action == "opened":
            record = {
                "author": author,
                "action_type": "pull_request",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            collection.insert_one(record)

        elif action == "closed" and pr.get("merged", False):
            record = {
                "author": author,
                "action_type": "merge",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            collection.insert_one(record)

    return jsonify({"status": "success"}), 200

@app.route("/api/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event["_id"] = str(event["_id"])
    return jsonify(events)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally
    app.run(host="0.0.0.0", port=port)
