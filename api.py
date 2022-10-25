from flask import Blueprint, request, jsonify
from LyricsFinder.app import LyricsFinder
from middlewares import enableCORS
import os
import requests, time

# The lyricsfinderapi blueprint

def LyricsFinderAPI():

    api_blueprint = Blueprint("lyrics-finder-api", __name__, url_prefix="/lyrics-finder-api")

    # GET KEYS from env
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


    # Get genius response time
    @api_blueprint.route("/get-genius-response-time/", methods=["get"])
    @enableCORS
    def getGeniusResponseTime():
        """ 
        This view or api is used to get a response time for how long it takes to get lyrics from a game
        This will be used by frontend to calculate an estimated duration
        """
        
        TOTAL_RESPONSE_TIME = 0  # In seconds

        # API response
        api_params = {
            "q": "juice wrld empty",
            "t": str(time.time())
        }
        api_headers = {
            "Authorization":  f"Bearer {GENIUS_ACCESS_TOKEN}",
            "Cache-Control": "max-age=0, no-cache, no-store",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        # Send request to the API endpoint
        api_response = requests.get("https://api.genius.com/search", params=api_params, headers=api_headers)

        TOTAL_RESPONSE_TIME += api_response.elapsed.total_seconds()

        # Genius response
        g_params = {
            "t": str(time.time())
        }
        g_headers = {
            "Cache-Control": "max-age=0, no-cache, no-store",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
        # Send request to the genius website itself
        g_response = requests.get("https://genius.com/Juice-wrld-empty-lyrics", params=g_params, headers=g_headers)

        TOTAL_RESPONSE_TIME += g_response.elapsed.total_seconds()

        return jsonify({
            "time": int(TOTAL_RESPONSE_TIME * 1000) # In ms
        })


    
    # Load complete playlist with tracks
    @api_blueprint.route("/load-complete-playlist/", methods=["get"])
    @enableCORS
    def loadCompletePlaylist():
        
        responseDict = {
            "status": -1,
            "message": "Required: 'url' get parameter is missing"
        }

        url = request.args.get("url")

        if url:
            
            # Initiate app
            app = LyricsFinder(CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN, False)

            # Try to get ID
            ID = app.parseSpotifyURL(url)

            # Check if url is valid
            if not url:
                responseDict["message"] = "Invalid URL"

            else:
                # Everything is fine, Proceed with loading playlist
                playlistResponse = app.loadPlaylist(url)

                if playlistResponse["status"] > 0 or playlistResponse["status"] == True:
                # Playlist loaded successfully
                    responseDict["status"] = 200 
                    responseDict["message"] = "Successfully loaded playlist"
                    responseDict["data"] = playlistResponse["data"]
                
                else:
                # Failed to load playlist
                    responseDict["message"] = playlistResponse["message"]

        
        return jsonify(responseDict)


    # Scan a song for keywords
    @api_blueprint.route("/scan-song/", methods=["get"])
    @enableCORS 
    def scanSong():

        # Get GET parameters
        songName = request.args.get("songname")
        artists = request.args.get("artists")
        keywords = request.args.get("keywords")

        # Check is songname get parameter exists
        if not songName:
            return jsonify({
                "status": -1,
                "message": "'songname' get parameter is missing."
            })

        # Check is artists get parameter exists
        if not artists:
            return jsonify({
                "status": -1,
                "message": "'artists' get parameter is missing."
            })

        # Check is keywords get parameter exists
        if not keywords:
            return jsonify({
                "status": -1,
                "message": "'keywords' get parameter is missing."
            })

        # Initiate app        
        app = LyricsFinder(CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN, False)

        scanResponse = app.scanSong(songName, artists, keywords)

        # If there is a response
        if scanResponse:
            
            returnDict = {
                "status": 200,
                "message": "Lyrics matched.",
                "data": scanResponse
            }

            return jsonify(returnDict)
        
        else:
            # No response
            return jsonify({
                "status": 0,
                "message": "No lyrics found for the given keyword(s)." 
            })




    return api_blueprint