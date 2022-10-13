import requests, base64, json, datetime
#from utils.utils import print_DT
from LyricsFinder.utils.utils import print_DT

class SpotifyAPI:

    def __init__(self, clientID, clientSecret, _print=False):
        self.print = _print
        self.clientID = clientID
        self.clientSecret = clientSecret

        if self.print: print("Setting up SpotifyAPI...\n")
        
        self.access_token = None
        # Get access token
        if self.checkForAccessTokens() == True:
            # Found a token
            pass
        else:
            # Get token
            self.getAccessToken()

    # Check for prestored access tokens
    def checkForAccessTokens(self):
        '''
        This method checks for (bearer) access tokens stored in access_token.json
        It also checks it's validity and returns False if the access token is invalid.
        '''
        if self.print: print_DT("Checking for cached access tokens...")
        try:
            with open('access_token.json', 'r') as access_token_json:
                data =  json.loads( access_token_json.read())
            
            # Check if access token exists
            if data["access_token"] == None:
                if self.print: print_DT("No access token found.")
                return False
            else:
                # Check for validity
                expires_at = data["expires_at"]
                date_expires_at = datetime.datetime.fromisoformat(expires_at)
                datenow = datetime.datetime.now()

                if datenow < date_expires_at:
                    # Access token is valid
                    if self.print: print_DT("Found a valid access token.")
                    self.access_token = data["access_token"]
                    return True

                else:
                    # Access token id not valid
                    if self.print: print_DT("Found access token but it is invalid.")
                    self.clearTokenSession()
                    return False

                

        except Exception:
            # If an error occurs when reading the access_token.json file, just get another one
            if self.print:
                print_DT("An error occured when trying to open access_token.json")
                print_DT("Preparing to get a new one.")
            return False


    # Get OAuth2.0 access token
    def getAccessToken(self):
        '''
        Documentation - https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
        '''
        # Format key
        key = f"{self.clientID}:{self.clientSecret}"
        ascii_key = key.encode("ascii")                     # Convert to bytes
        base64_encoded_key = base64.b64encode(ascii_key)    # Encode using base64 encoding
        final_key = base64_encoded_key.decode("utf-8")      # Convert to a string from bytes
        # Request endpoint, body and header
        endpoint = "https://accounts.spotify.com/api/token"
        body = {
            "grant_type": "client_credentials"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {final_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        # Send request
        if self.print: print_DT("Getting access token...")
        response = requests.post(endpoint, data=body, headers=headers)
        # Convert response to json
        responseJson = json.loads(response.text)

        # Process response
        if response.status_code != 200:
            # Print error details and raise exception
            if self.print:
                print_DT("Failed to get OAuth access token. Please check if you have provided your client credentials correctly.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['error']}")

            # Failed to get a token
            return False

        else:
            # Store access token
            if self.print: print_DT("Successfully received access token.")
            self.access_token = responseJson["access_token"]
            self.updateAccessToken(responseJson)

            # Successfully retrieved a valid token
            return True


    # Update access_token.json
    def updateAccessToken(self, responseJson):
        '''
        This method stores all the relevant details about the access token in access_token.json
        access_token.json MUST BE IN .gitignore
        '''
        received_at = datetime.datetime.now()
        expires_at = received_at + datetime.timedelta(seconds=responseJson["expires_in"]) 
        access_tokenJSON = {
            "type": responseJson["token_type"],
            "access_token": responseJson["access_token"],
            "received_at": received_at.__str__(),
            "duration": responseJson["expires_in"],
            "expires_at": expires_at.__str__()
        }

        access_token_STRINGIFIED = json.dumps(access_tokenJSON, indent=4)

        if self.print: print_DT("Storing token details in access_token.json... probably not the safest thing to do...")
        # Write to file
        with open("access_token.json", "w") as token_File:
            token_File.write(access_token_STRINGIFIED)
        if self.print: print_DT("Storing complete.")


    # Clears token session
    def clearTokenSession(self):
        '''
        This method clears the token currently stored in access_token.json file
        '''
        access_tokenJSON = {
            "type": None,
            "access_token": None,
            "received_at": None,
            "duration": None,
            "expires_at": None
        }
        access_token_STRINGIFIED = json.dumps(access_tokenJSON, indent=4)

        if self.print: print_DT("Clearing token details...")
        # Overwrite to file
        with open("access_token.json", "w") as token_File:
            token_File.write(access_token_STRINGIFIED)
        if self.print: print_DT("Details cleared.")


    # Get bearer headers
    def getBearerHeaders(self):
        '''
        This method returns the a header object with Authorization key and bearer access token
        '''
        if self.access_token != None:
            headers = {
                'Authorization': f"Bearer {self.access_token}"
            }

            return headers
        else:
            return None


