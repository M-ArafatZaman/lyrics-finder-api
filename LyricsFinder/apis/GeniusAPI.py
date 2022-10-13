import requests, json
import time
#from utils.utils import print_DT
from LyricsFinder.utils.utils import print_DT

class GeniusAPI:
    '''
    This class connects to the genius API using just a "semi-public" access token so it can only access endpoints
    which are not private. 
    '''
    def __init__(self, access_token, _print=True):
        self.access_token = access_token
        self.print = _print


    def searchSongs(self, searchTerm, cache=True):
        '''
        This method searches for songs using the searchTerm from the genius API.
        Documentation - https://docs.genius.com/#search-h2
        '''
        endpoint = "https://api.genius.com/search"
        params = {
            "q": searchTerm
        }
        # Add a timestamp if cache is false
        if not cache: params["time"] = str(time.time())

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        # Send request
        response = requests.get(endpoint, params=params, headers=headers)
        responseJson = json.loads(response.text)

        if response.status_code != 200:
            # Failed request
            if self.print:
                print_DT(f"Failed to retrieve song '{searchTerm}'.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['meta']['message']}")
            
            # Just return an empty list so that it is handled as if there were no hits
            return []
        else:
            # Successfully retrieved song
            
            return responseJson["response"]["hits"]
