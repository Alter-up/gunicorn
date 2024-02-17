from flask import Flask
import os

app = Flask(__name__)

@app.route('/callback')
def hello_world():
    return 'Hello, world!'
