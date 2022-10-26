from datetime import datetime
import itertools
import hashlib
import logging
import random
import string
import json

logger = logging.getLogger(__name__)


class Message:
    MALWARE_SIGNATURE = "H4CK3R"
    device_names = [
        "IDS_SERVER",
        "VCONTROLLER_GOOGLE",
        "VCONTROLLER_AMAZON",
        "CONTROLLER_RING",
        "CONTROLLER_NEST_SMOKE",
        "CONTROLLER_NEST_CAMERA",
        "CONTROLLER_ROOMBA",
        "CONTROLLER_UNIVERSAL_REMOTE",
        "CONTROLLER_OVEN",
        "CONTROLLER_MRCOFFEE",
    ]
    new_id = itertools.count().__next__

    def __init__(self, origin: str, target: str, text: str) -> None:
        self.index = Message.new_id()
        self.origin = origin
        self.target = target
        self.text = text
        self.timestamp = datetime.now().strftime("%x %X")
        self.signature = self.__assign_signature()

    def __assign_signature(self) -> str:
        signature = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        if self.index > 0:
            if random.randint(0, 5) > 4:
                signature = signature.replace(signature[:6], self.MALWARE_SIGNATURE)
        return signature

    @property
    def __key(self):
        return (
            self.index,
            self.origin,
            self.target,
            self.text,
            self.timestamp,
            self.signature,
        )

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Message):
            return self.__key == __o.__key
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__key)

    def get_hash(self) -> str:
        msg_string = json.dumps(self.__key, sort_keys=True).encode()
        return hashlib.sha256(msg_string).hexdigest()

    def to_json(self):
        return json.dumps(self.__key, sort_keys=True, indent=4)

    def scan_message(self) -> bool:
        return self.signature.startswith(self.MALWARE_SIGNATURE)
