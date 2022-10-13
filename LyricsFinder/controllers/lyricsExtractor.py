import re

def getTopLyricsUrl(apiResponse, songName: list, artists: list):
    '''
    This function works with the "hits" attribute from the genius search API - https://docs.genius.com/#search-h2
    It returns the url in string format of the top most search result
    '''
    # Iterate through each hits
    for hit in apiResponse:
        # Convert artists into a string and again to split at every whitespace
        artist = " ".join(artists)
        artists = artist.split()

        # If current hit is a song, extract details, or else go next
        # Also check if the artist names and the song name atleast "SOMEWHAT" matches
        if hit['type'] == "song" and checkForMatch(songName, hit["result"]["title"].split()) and checkForMatch(artists, hit["result"]["artist_names"].split()):
           return hit['result']['url'] 
        else:
            continue
    
    # If no match, return None
    return None


## This function returns true if the two arrays have atleast something in common
def checkForMatch(arr1: list, arr2: list) -> bool:
    # Lower strings for fair comparison
    _arr1 = [removeBrackets(x.lower()) if type(x) == str else x for x in arr1]
    _arr2 = [removeBrackets(x.lower()) if type(x) == str else x for x in arr2]

    return len(set(_arr1).intersection(set(_arr2))) > 0


## This function removes brackets
def removeBrackets(txt) -> str:
    # Group brackets
    return re.sub(r"[()]", "", txt)