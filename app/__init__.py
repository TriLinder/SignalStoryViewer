from flask import Flask, send_from_directory, make_response
from flask_svelte import render_template
import os

from .config import SIGNAL_CLI_DIRECTORY, PHONE_NUMBER
from .database import Database
from .signal_client import SignalClient

app = Flask(__name__)

db = Database("db.json")
if not "stories" in db.data:
    db.data["stories"] = {}

signal_client = SignalClient(db, PHONE_NUMBER)

@app.route('/')
def index():
    return render_template('index.html')

@app.get("/stories")
def get_stories():
    return list(db.data["stories"].values())

@app.route("/story/<story_id>/view")
def story_view(story_id):
    story = db.data["stories"][story_id]

    if not story["viewed"]:
        signal_client.send_view_receipt(story["sender"]["number"], story["timestamp"])
        db.data["stories"][story_id]["viewed"] = True
        db.save_to_disk()

    return make_response("", 204)

@app.get("/story/<story_id>/media")
def get_story_media(story_id):
    filename = db.data["stories"][story_id]["media"]
    return send_from_directory(os.path.join(SIGNAL_CLI_DIRECTORY, "attachments"), filename)

@app.get("/story/<story_id>/avatar")
def get_story_sender_avatar(story_id):
    sender = db.data["stories"][story_id]["sender"]["number"]
    return send_from_directory(os.path.join(SIGNAL_CLI_DIRECTORY, "avatars"), f"profile-{sender}")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)