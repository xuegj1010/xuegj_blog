from config import DevConfig

from flask import Flask
import wtforms


app = Flask(__name__)

app.config.from_object(DevConfig)

views = __import__('views')
