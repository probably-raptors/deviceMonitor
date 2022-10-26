from .assets.Blockchain import Blockchain
from .assets.Message import Message
from .assets.Block import Block
from flask import render_template
from app import app
import logging
import random
import string


blockchain = Blockchain()
logger = logging.getLogger(__name__)


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    most_recent_block = next(iter(blockchain.blocks.values()))
    most_recent_block: Block
    messages = [message for message in most_recent_block.ledger.values()][1:]

    return render_template(
        "_dashboard.html",
        messages=messages,
        title="Dashboard",
    )


@app.route("/captures", methods=["POST", "GET"])
def captures():
    return render_template(
        "_captures.html",
        captures=blockchain.captures,
        title="Captures",
    )


@app.route("/send", methods=["POST", "GET"])
def send():
    origin = random.choice(Message.device_names)
    target = random.choice(Message.device_names)
    while target == origin:
        target = random.choice(Message.device_names)
    text = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    message = Message(origin, target, text)

    if Message.scan_message(message):
        blockchain.capture_message(message)
        return {
            "captures": [capture.to_json() for capture in blockchain.captures],
            "is_malicious": True,
        }
    blockchain.mine_block(message)
    data = f"""
    <div class="dashboard-row">
        <div class="three columns" name="timestamp">
            <p>[{message.timestamp}]</p>
        </div>
        <div class="three columns" name="signature">
            <p>{message.signature}</p>
        </div>
        <div class="three columns" name="origin">
            <p>{message.origin}</p>
        </div>
        <div class="three columns" name="target">
            <p>{message.target}</p>
        </div>
    </div>
    """
    is_malicious = False

    return {
        "data": data,
        "is_malicious": is_malicious,
    }
