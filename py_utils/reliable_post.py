import json
from abc import ABC
from enum import Enum
from typing import Any


class MessageState(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    PENDING = 'pending'


class Message:
    def __init__(self, url: str, body: Any, state: MessageState = MessageState.PENDING):
        self.url = url
        self.body = body
        self.state = state

    def dumps(self):
        return json.dumps({"url": self.url, "body": self.body, "state": self.state})

    @classmethod
    def loads(cls, text: str):
        the_json = json.loads(text)
        return Message(url=the_json.get("url", None),
                       body=the_json.get("body", None),
                       state=the_json.get("state", MessageState.PENDING))


class MessageQueue(ABC):

    def __init__(self, max_retry: int):
        self.max_retry = max_retry

    def add(self, message: Message):
        pass

    def remove(self, message: Message):
        pass

    def on_exceed_max_retry(self, message: Message):
        pass
