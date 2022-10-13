from flask import Blueprint, request, jsonify
from LyricsFinder.app import LyricsFinder
from middlewares import enableCORS
import os

# The lyricsfinderapi blueprint

def LyricsFinderAPI():

    api_blueprint = Blueprint("lyrics-finder-api", __name__, url_prefix="/lyrics-finder-api")

    # GET KEYS from env
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


    # Load playlist
    @api_blueprint.route("/load-playlist/", methods=["get"])
    @enableCORS
    def loadPlaylist():
        '''
        This endpoint is the first step of the app. It fetches basic playlist data.

        '''

        responseDict = {
            "status": -1,
            "message": "Required: 'url' get parameter is missing"
        }

        ## Try to get url
        url = request.args.get("url")
        
        if url:
            
            # Initiate app
            app = LyricsFinder(CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN, False)

            # Get ID
            ID = app.parseSpotifyURL(url.strip())

            # If ID is none, it was an invalid url
            if ID == None:
                responseDict["message"] = "Invalid URL"

            # Get playlist detail
            playlistDetails = app.SpotifyAPI.getPlaylistDetailsByID(ID)

            # Check response
            if playlistDetails["status"]:

                responseDict["status"] = 200
                responseDict["message"] = "Successfully loaded playlist"
                responseDict["data"] = playlistDetails["data"]
                
            else:
                # Response was unsuccessful
                responseDict["message"] = "Unsuccessful"

        return jsonify(responseDict)


    # Search playlist
    @api_blueprint.route("/search-playlist/", methods=["get"])
    @enableCORS
    def searchPlaylist():
        '''
        This endpoint is the 2nd step of the app.
        It takes the URL AND a search term and performs a search.
        '''

        # The response dict
        responseDict = {
            "status": -1,
            "message": "NULL"
        }

        # Get query parameters
        search = request.args.get("search")
        url = request.args.get("url")

        # Initiate app
        app = LyricsFinder(CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN, False)

        # If search exists
        if search:
            # Check if search has some valid terms
            if len(search) <= 0:
                responseDict["message"] = "Enter search terms"
        
        else:
            # No search parameter
            responseDict["message"] = "Required: 'search' get parameter is missing."

        # If url exists, and if it is a valid url
        if url:
            ID = app.parseSpotifyURL(url)

            if ID == None:
                responseDict["messagge"] = "Enter a valid URL."

        else:
            responseDict["message"] = "Required: 'url' get parameter is missing."



        # Both url and search is available
        if search and url:
            searchResult = app.searchPlaylist(url, search)

            responseDict = {
                "status": 200,
                "message": "Successfully scanned playlist",
                "data": searchResult
            }

        return jsonify(responseDict)



    return api_blueprint