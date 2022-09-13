from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Load Environment variables
load_dotenv('.env')

SECRET_KEY = os.getenv("APP_SECRET_KEY")

# Setup server
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route('/')
def index():
    return {"hello": "world"}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 