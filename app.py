from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv
import os
from middlewares import enableCORS
from api import LyricsFinderAPI

# Load Environment variables
load_dotenv('.env')

SECRET_KEY = os.getenv("APP_SECRET_KEY")

# Function to create the app
def create_app():

    # Setup server
    app = Flask(__name__, static_folder="web/static/", static_url_path="/static", template_folder="web")
    app.config["SECRET_KEY"] = SECRET_KEY

    BASE_URI = "/lyrics-finder-api/"
    # load-playlist/
    # search-playlist/
    # get-genius-response-time/

    @app.route('/')
    @enableCORS
    def index():
        response = jsonify({"hello": "world"})
        return response

    # A route to ping and check if all systems are operational
    @app.route('/ping/')
    @enableCORS
    def ping():
        return jsonify({"status": "OK"})
    
    # Register lyricsfinder blueprint
    LF_BP = LyricsFinderAPI()
    app.register_blueprint(LF_BP)


    return app


if __name__ == '__main__':

    app = create_app()
    app.run(host='127.0.0.1', port=8000, debug=True)
 