import json
from abc import ABC
from enum import Enum
from typing import Any


class MessageState(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    PENDING = 'pending'


class Message:
    def __init__(self, id: str, url: str, body: Any, state: MessageState = MessageState.PENDING):
        self.url = url
        self.body = body
        self.state = state
        self.id = id

    def dumps(self):
        return json.dumps({"id": self.id, "url": self.url, "body": self.body, "state": self.state})

    @classmethod
    def loads(cls, text: str):
        the_json = json.loads(text)
        return Message(id=the_json["id"],
                       url=the_json["url"],
                       body=the_json["body"],
                       state=the_json["state"])


class AbstractMessageQueueStorage(ABC):
    pass


class MessageQueueStorage(AbstractMessageQueueStorage):
    def __init__(self):
        self.queue = []

    def add(self, message: Message):
        self.queue.append(message)


class MessageQueue(ABC):

    def __init__(self, max_retry: int):
        self.max_retry = max_retry

    def add(self, message: Message):
        pass

    def remove(self, message: Message):
        pass

    def on_exceed_max_retry(self, message: Message):
        pass
