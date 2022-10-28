from collections import OrderedDict
from .Message import Message
from .Block import Block
import logging

logger = logging.getLogger(__name__)


class Blockchain:
    def __init__(self, difficulty=2) -> None:
        self.difficulty = difficulty
        self.blocks = OrderedDict()
        self.captures = []
        self.__create_genesis_block()

    @property
    def last_block(self) -> Block:
        return self.blocks[next(reversed(self.blocks))]

    def __create_genesis_block(self) -> None:
        message = Message("IDS_SERVER", "IDS_SERVER", "Genesis Block")
        genesis_block = Block("0" * self.difficulty)
        genesis_hash = self.__proof_of_work(genesis_block)
        self.blocks[str(genesis_hash)] = genesis_block
        self.update_ledgers(message)

    def __proof_of_work(self, block: Block) -> int:
        new_hash = str(block.get_hash())
        while not new_hash.startswith("0" * self.difficulty):
            block.nonce += 1
            new_hash = str(block.get_hash())
        return new_hash

    def capture_message(self, message: Message) -> None:
        self.captures.append(message)

    def update_ledgers(self, message: Message) -> None:
        for block in self.blocks.values():
            block: Block
            block.update_ledger(message)
            # block.ledger[message.get_hash()] = message

    def mine_block(self, message: Message) -> Block:
        new_block = Block(next(reversed(self.blocks)))
        new_hash = self.__proof_of_work(new_block)
        logger.info(f"New hash [{new_hash}] found for block")
        self.blocks[new_hash] = new_block
        logger.info(f"New message #{message.index} added to local ledger")
        self.update_ledgers(message)
        logger.info(f"Ledgers updated")
        return new_block
