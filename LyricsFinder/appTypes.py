from typing import List, Sequence
from dataclasses import dataclass

@dataclass
class SnippetType:
    keyword: str
    snippet: str

@dataclass
class ArtistType:
    name: str

@dataclass
class ReturnedLyrics:
    '''
    Data type for the songs returned whose lyrics matches the keyword
    '''
    name: str
    lyrics: str
    snippets: Sequence[SnippetType]
    imageURL: str
    artists: str
    url: str
    previewURL: str
    geniusURL: str

    