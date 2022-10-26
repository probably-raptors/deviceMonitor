from logging.config import dictConfig
from config import Config
from flask import Flask
import logging

app = Flask(__name__)
# app.config.from_object(Config)
dictConfig(Config.LOG_CONFIG)
app.logger.info("application startup")

if app.debug:
    wkz = logging.getLogger("werkzeug")
    wkz.setLevel(logging.ERROR)

from app import routes
