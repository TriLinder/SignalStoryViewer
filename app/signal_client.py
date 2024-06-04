import subprocess
import json
import uuid
import time
import os

from .database import Database
from .config import SIGNAL_CLI_DIRECTORY

class SignalClient:
    def __init__(self, db: Database, phone_number: str) -> None:
        self.db = db
        self.phone_number = phone_number

    def recieve_messages(self) -> None:
        result = subprocess.run(["flatpak run org.asamk.SignalCli",  "--output=json",  "-a", self.phone_number, "receive"], capture_output=True, text=True)
        messages = []

        for line in result.stdout.split("\n"):
            try:
                messages.append(json.loads(line))
            except:
                print(f"Recieved non-JSON line of output, ignoring: `{line}`")

        #Process the incoming messages
        for message in messages:
            if "envelope" in message:
                if "storyMessage" in message["envelope"]:
                    self.process_story_message(message)
                elif "dataMessage" in message["envelope"]:
                    self.process_data_message(message)
                else:
                    print(f"Unknown message: `{message}`")

                time.sleep(0.25)    

    def process_story_message(self, message) -> None:
        print(f"Processing story message: `{message}`")
        envelope = message["envelope"]

        story_id = uuid.uuid4().hex

        self.db.data["stories"][story_id] = {
            "id": story_id,
            "timestamp": envelope["timestamp"],
            "sender": {
                "number": envelope["sourceNumber"],
                "name": envelope["sourceName"],
            },
            "media": {
                "type": envelope["storyMessage"]["fileAttachment"]["contentType"].split("/")[0],
                "filename": envelope["storyMessage"]["fileAttachment"]["id"]
            },
            "caption": envelope["storyMessage"]["fileAttachment"]["caption"],
            "viewed": False
        }

        self.db.save_to_disk() #Simply changing the dictionary does not trigger a database re-save on its own

    def process_data_message(self, message):
        print(f"Processing data message: `{message}`")
        dataMessage = message["envelope"]["dataMessage"]

        if "remoteDelete" in dataMessage:
            try:
                timestamp = dataMessage["remoteDelete"]["timestamp"]
                story_id = self.get_story_id_from_timestamp(timestamp)
                self.delete_story(story_id)
            except Exception as e:
                print(f"Failed to delete story based on remote data message: {e}")
        else:
            print("Unknown data message")

    def send_view_receipt(self, sender_number, message_timestamp):
        print("Sending view receipt")
        result = subprocess.run([SIGNAL_CLI_PATH, "--output=json", "-a", self.phone_number, "sendReceipt", "--type", "viewed", sender_number, "-t", str(message_timestamp)], capture_output=True, text=True)
        print(result.stdout, result.stderr)

    def get_story_id_from_timestamp(self, timestamp):
        for story_id, story in dict(self.db.data["stories"]).items():
            if story["timestamp"] == timestamp:
                return story_id
        
        raise KeyError

    def delete_story(self, story_id):
        print(f"Deleting story: {story_id}")

        media_filename = self.db.data["stories"][story_id]["media"]["filename"]
        try:
            os.remove(os.path.join("flatpak run org.asamk.SignalCli", "attachments", media_filename))
        except Exception as e:
            print(f"Failed to delete story media: {e}")
        self.db.data["stories"].pop(story_id, None)

        self.db.save_to_disk()