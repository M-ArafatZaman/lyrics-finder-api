from .users import SpotifyUserAPI
import requests, json
#from utils.utils import print_DT
#from controllers.query import parseDictToQuery

from LyricsFinder.utils.utils import print_DT
from LyricsFinder.controllers.query import parseDictToQuery

class SpotifyPlaylistAPI(SpotifyUserAPI):
    '''
    This class inherits from the parent SpotifyAPI class
    '''
    def __init__(self, clientID, clientSecret, _print=False):
        super().__init__(clientID, clientSecret, _print)

    
    # Get playlist by ID
    def getPlaylistByID(self, id):
        '''
        This API gets details from getPlaylistDetailsByID and retrieveTracksFromPlaylistID, and combines them
        '''

        details = self.getPlaylistDetailsByID(id)
        tracks = self.getTracksFromPlaylistID(id)

        returnData = {
            "status": False
        }
        
        if details["status"] == True:
            returnData["status"] = True
            returnData["data"] = {
                "playlist": details["data"],
                "has_all_tracks": tracks["has_all_tracks"],
                "items": tracks["tracks"]
            }

        return returnData

    
    # Get playlist details from the api 
    def getPlaylistDetailsByID(self, id):
        '''
        Documentation - https://developer.spotify.com/console/get-playlist/

        Fields=external_urls,name,images,owner(display_name,id)
        '''
        # Create query | Retrieve only required fields
        queryFields = {
            "external_urls": str,
            "description": str,
            "name": str,
            "images": str,
            "owner": {
                "display_name": str,
                "id": str
            },
            "followers": {
                "total": int
            },
            "tracks": {
                "total": int
            }
        }

        query = parseDictToQuery(queryFields)
        

        returnData = {
            "status": False,
            "data": {}
        }

        # Even though this endpoint contains tracks, it will only be used to collect basic playlist info.
        endpoint = f'https://api.spotify.com/v1/playlists/{id}'
        headers = self.getBearerHeaders()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        parameters = {
            "fields": query
        }

        # Send request
        if self.print: print_DT("Retrieving playlist details...")

        response = requests.get(endpoint, headers=headers, params=parameters)
        # Convert response to json
        responseJson = json.loads(response.text)

        # Process response
        if response.status_code != 200:
            # Failed to get playlist details
            if self.print:
                print_DT("Failed to retrieve playlist details.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['error']['message']}")
            
            return returnData

        else:
            # Playlist details has been successfully retrieved
            if self.print: print_DT(f"Successfully retrieved playlist details => {responseJson['name']} by {responseJson['owner']['display_name']}")

            if self.print: print_DT(f"Retrieving tracks from '{responseJson['name']}'...")


            returnData["status"] = True
            returnData["data"] = responseJson

            # Get owner details
            ownerDetailsResponse = self.getUserByID(responseJson["owner"]["id"])
            if ownerDetailsResponse["status"] == True:
                # Successfully retrieved owner details
                returnData["data"]["owner"] = ownerDetailsResponse["data"]

            return returnData


    def getTracksFromPlaylistID(self, id):
        '''
        https://developer.spotify.com/console/get-playlist-tracks/

        Fields = items(track(album(images),artists(name),external_urls,name)),next
        '''
        # Create and parse query
        queryFields = {
            "items": {
                "track": {
                    "album": {
                        "images": str
                    },
                    "artists": {
                        "name": str
                    },
                    "external_urls": str,
                    "name": str,
                    "preview_url": str
                }
            },
            "next": str
        }

        query = parseDictToQuery(queryFields)

        endpoint = f"https://api.spotify.com/v1/playlists/{id}/tracks"

        parameters = {
            "fields" : query
        }

        trackItems = self.recursivelyRetrieveTracksFromPlaylistEndpoint(endpoint, parameters)

        return trackItems

    def recursivelyRetrieveTracksFromPlaylistEndpoint(self, endpoint, parameters={}):
        '''
        This method executes the get request to retrieve the playlist
        Since the spotify API only returns a maximum of 100 tracks per API hit,
        it also checks if there are any more tracks left to retrieve.
        '''
        trackItems = []

        headers = self.getBearerHeaders()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

        # Send request and convert response to json
        response = requests.get(endpoint, headers=headers, params=parameters)
        responseJson = json.loads(response.text)

        # Process response
        if response.status_code != 200:
            # If an error occurs
            if self.print:
                print_DT("Failed to retrieve all tracks.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['error']['message']}")
            
            return {
                "has_all_tracks": False,
                "tracks": None
            }
        
        else:
            # Successfully received tracks    
            nextEndpoint = responseJson["next"]
            trackItems = responseJson["items"]
            
            if nextEndpoint == None:
                # All tracks has been retrieved
                if self.print: print_DT("All tracks has been retrieved.")

                return {
                    "has_all_tracks": True,
                    "tracks": trackItems
                }
            
            else: 
                nextTracks = self.recursivelyRetrieveTracksFromPlaylistEndpoint(nextEndpoint, parameters)

                # If there ARE tracks from the nextEndpoint, combine them
                totalTracks = trackItems
                if type(nextTracks["tracks"]) == list:
                    totalTracks = trackItems + nextTracks["tracks"]

                if nextTracks["has_all_tracks"] == True:
                    # all next tracks has been successfully retrieved
                    return {
                        "has_all_tracks": True,
                        "tracks": totalTracks
                    }
                
                else:
                    # Not all tracks have been retrieved
                    return {
                        "has_all_tracks": False,
                        "tracks": totalTracks
                    }
