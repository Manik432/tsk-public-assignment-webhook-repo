from datetime import datetime, timezone
from pydantic import BaseModel
import json
import datetime
import time

class Action():
    def  __init__(self, request_id, author, action, from_branch, to_branch):
        self.request_id = request_id
        self.author = author
        self.action = action
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = datetime.datetime.now(timezone.utc)


    def to_document(self):

        return dict(
            request_id = self.request_id,
            author = self.author,
            action = self.action,
            from_branch = self.from_branch,
            to_branch = self.to_branch,
            timestamp = self.timestamp
        )


    def to_json(self):
        return json.dumps(self)