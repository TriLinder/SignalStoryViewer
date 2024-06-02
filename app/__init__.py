from flask import Flask, send_from_directory, make_response
from flask_svelte import render_template
import os
import time
import threading

from .config import SIGNAL_CLI_DIRECTORY, PHONE_NUMBER, PROCESSING_INTERVAL
from .database import Database
from .signal_client import SignalClient

app = Flask(__name__)

db = Database("db.json")
if not "stories" in db.data:
    db.data["stories"] = {}

signal_client = SignalClient(db, PHONE_NUMBER)

last_processing_thread_timestamp = 0

def processing_thread():
    global last_processing_thread_timestamp

    while True:
        print("Processing started")
        start_time = time.time()

        if not start_time - last_processing_thread_timestamp > PROCESSING_INTERVAL - 1:
            continue

        last_processing_thread_timestamp = start_time

        try:
            #Delete old (> 24h) stories
            stories_to_delete = []
            for story_id, story in dict(db.data["stories"]).items():
                if (story["timestamp"] / 1000) + 24*60*60 < time.time():
                    stories_to_delete.append(story_id)

            for story_id in stories_to_delete:
                print(f"Deleting old story: {story_id}")
                media_filename = db.data["stories"][story_id]["media"]["filename"]
                os.remove(os.path.join(SIGNAL_CLI_DIRECTORY, "attachments", media_filename))
                db.data["stories"].pop(story_id, None)

            #Recieve new stories
            signal_client.recieve_messages()

            #Make sure everything's saved
            db.save_to_disk()
        except Exception as e:
            print(e)

        print(f"Processing finished after {round(time.time() - start_time, 2)}s")
        time.sleep(PROCESSING_INTERVAL)

@app.route('/')
def index():
    return render_template('index.html')

@app.get("/stories")
def get_stories():
    return sorted(list(db.data["stories"].values()), key=lambda story: story["timestamp"], reverse=True)

@app.route("/story/<story_id>/view")
def story_view(story_id):
    story = db.data["stories"][story_id]

    if not story["viewed"]:
        db.data["stories"][story_id]["viewed"] = True
        db.save_to_disk()
        signal_client.send_view_receipt(story["sender"]["number"], story["timestamp"])

    return make_response("", 204)

@app.get("/story/<story_id>/media")
def get_story_media(story_id):
    filename = db.data["stories"][story_id]["media"]["filename"]
    return send_from_directory(os.path.join(SIGNAL_CLI_DIRECTORY, "attachments"), filename)

@app.get("/story/<story_id>/avatar")
def get_story_sender_avatar(story_id):
    sender = db.data["stories"][story_id]["sender"]["number"]
    return send_from_directory(os.path.join(SIGNAL_CLI_DIRECTORY, "avatars"), f"profile-{sender}")

if True or __name__ == "__name__":
    threading.Thread(target=processing_thread).start()
    app.run(port=5000, threaded=True, debug=False)