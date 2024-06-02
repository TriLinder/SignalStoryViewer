import json
import os
import shutil
import time
import uuid
import threading
from collections import deque

class ObservableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = None

    def __setitem__(self, __key: any, __value: any) -> None:
        super().__setitem__(__key, __value)

        if self.callback:
            self.callback(__key, __value)

    def set_callback(self, callback: callable):
        self.callback = callback

class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self.queue = []

        #Load the database file
        if os.path.isfile(self.path):
            with open(self.path, 'r') as f:
                self.data: dict = ObservableDict(json.load(f)['data'])
        else:
            self.data = ObservableDict({})

        #Set callback for data changes
        self.data.set_callback(self.on_data_change)

    def on_data_change(self, key, value):
        #It's time to save to disk
        self.save_to_disk()

    def save_to_disk(self):
        thread = threading.Thread(target=self._save_to_disk)
        thread.start()

    def _save_to_disk(self):
        #First, let us prepare our output, to make sure it doesn't change, before we reach our turn
        queue_key = uuid.uuid4()
        output = {
                'metadata': {
                    'time': time.time(),
                    'queue_key': queue_key.hex
                },
                'data': self.data
            }

        #Add ourself to the queue and wait for our turn
        self.queue.append(queue_key)
        
        while self.queue[0] != queue_key:
            time.sleep(0.01)

        #It's our turn! First make a copy of the file, if it exsits
        if os.path.isfile(self.path):
            shutil.copy2(self.path, f'{self.path}.old')

        #Now save our changes to disk
        with open(self.path, 'w') as f:
            json.dump(output, f, ensure_ascii=True, separators=(',', ':'))