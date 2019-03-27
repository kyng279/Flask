from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
app.run(host='0.0.0.0')

from app import routes
