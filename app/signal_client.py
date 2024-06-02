import subprocess
import json
import uuid

from .database import Database

class SignalClient:
    def __init__(self, db: Database, phone_number: str) -> None:
        self.db = db
        self.phone_number = phone_number

    def recieve_messages(self) -> None:
        result = subprocess.run(f"signal-cli --output=json -a {self.phone_number} receive", capture_output=True, text=True, shell=True)
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

    def send_view_receipt(self, sender_number, message_timestamp):
        print("Sending view receipt")
        result = subprocess.run(f'signal-cli --output=json -a {self.phone_number} sendReceipt --type viewed "{sender_number}" -t {message_timestamp}', capture_output=True, text=True, shell=True)
        print(result.stdout, result.stderr)