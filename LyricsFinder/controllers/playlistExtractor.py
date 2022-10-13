# Static typing
from typing import List

def getTrackName(apiResponse) -> List[str]:
    '''
    This function returns the string name of a single track from the reponse provided by the spotify API.
    https://developer.spotify.com/console/get-playlist-tracks/
    '''
    name = apiResponse['track']['name']
    artists = []

    # Iterate through each artist
    for artist in apiResponse['track']['artists']:
        artists.append(artist['name'])
    
    artistName = ', '.join(artists)

    return f"{artistName} - {name}"

