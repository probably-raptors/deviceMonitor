from collections import OrderedDict
from .Message import Message
from hashlib import sha256
import itertools
import json


class Block:
    new_id = itertools.count().__next__

    def __init__(self, previous_hash: str):
        self.index = Block.new_id()
        self.previous_hash = previous_hash
        self.nonce = 0
        self.ledger = OrderedDict()

    @property
    def __key(self):
        return (
            self.index,
            self.previous_hash,
            self.nonce,
            [message.get_hash() for message in self.ledger.values()],
        )

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Block):
            return self.__key == __o.__key
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__key)

    def get_hash(self) -> str:
        block_string = json.dumps(self.__key, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def update_ledger(self, message: Message) -> None:
        self.ledger[message.get_hash()] = message
