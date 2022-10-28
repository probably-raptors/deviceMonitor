from logging.config import dictConfig
from config import Config
from flask import Flask
import logging

app = Flask(__name__)
dictConfig(Config.LOGGING_CONFIG)
app.logger.info("application startup")

from app import routes
