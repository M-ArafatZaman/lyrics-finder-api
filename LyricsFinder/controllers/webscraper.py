import requests, bs4
import time


def scrapeLyricsFromURL(url, cache=True):
    '''
    This function scrapes the genius url for lyrics and returns it.
    '''
    lyrics: str = ""

    params = {}
    # Add a timestamp if cache is false
    if not cache: params["time"] = str(time.time())
    # Browser like header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, params=params, headers=headers)

    # Convert response to bs4 object
    bs4Object = bs4.BeautifulSoup(response.content, "html.parser")

    for each in bs4Object.find_all("div", {"data-lyrics-container": "true"}):
        adjustLines = str(each).replace("\n", "").replace("<br/>", "\n")
        finalLyrics = bs4.BeautifulSoup(adjustLines, "html.parser")
        lyrics += finalLyrics.get_text()
        lyrics += "\n"

    return lyrics



