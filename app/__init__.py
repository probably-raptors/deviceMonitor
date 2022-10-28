from logging.config import dictConfig
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
dictConfig(Config.LOGGING_CONFIG)

from app import routes
