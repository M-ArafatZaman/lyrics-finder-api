from .main import SpotifyAPI
import requests, json
#from utils.utils import print_DT
from LyricsFinder.utils.utils import print_DT

class SpotifyUserAPI(SpotifyAPI):
    '''
    This class inherits from the parent SpotifyAPI class and implements User based classes
    '''
    def __init__(self, clientID, clientSecret, _print=False):
        super().__init__(clientID, clientSecret, _print)
    

    # Get user
    def getUserByID(self, user_id):
        '''
        This method retrieves a user's profile details - https://developer.spotify.com/console/get-users-profile/
        '''
        returnData = {
            "status": False,
            "data": {}
        }

        endpoint = f"https://api.spotify.com/v1/users/{user_id}"
        headers = self.getBearerHeaders()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

        # Send get request
        response = requests.get(endpoint, headers=headers)
        # Get json
        responseJson = json.loads(response.text)

        # Process response
        if response.status_code != 200:
            if self.print:
                print_DT("Failed to retrieve playlist details.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['error']['message']}")
            
            return returnData
        
        else:
            # The request was a success
            if self.print: print_DT(f"Successfully received {responseJson['display_name']}'s details")

            data = {
                "name": responseJson['display_name'],
                "url": responseJson["external_urls"]["spotify"],
                "images": responseJson["images"]
            }

            returnData["status"] = True
            returnData["data"] = data

            return returnData
            
