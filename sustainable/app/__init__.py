from unittest.mock import MagicMock

from flask import Flask
from sustainable.config import Config
from sustainable.scraping.spyders import SpyderWeb
import os
import pyrebase

app = Flask(__name__)
app.config.from_object(Config)

# database init
firebase = pyrebase.initialize_app(Config.fb_config)



# Temporarily replace quote function
def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote
auth = firebase.auth()
db = firebase.database()

spyder_web = SpyderWeb()

from sustainable.app import routes, models

