from datetime import datetime
from typing import List
from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class AddingReleaseTrack(TunedModel):
    track_num: int
    track_title: str
    genre: List
    bitrate: str
    file_size: int
    duration: int

class AddingRelease(TunedModel):
    artist: str
    album: str
    release_date: str
    tracks: List[AddingReleaseTrack]
