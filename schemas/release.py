from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ReleaseTypeSchema(TunedModel):
    id: int
    name: str

class TrackSchemaBeforeInsert(TunedModel):
    name: str
    artists_id_list: list[int]
    release_date: Optional[datetime] = None
    releases_id: Optional[int] = None
    number: int
    duration: int
    bitrate: int
    file_size: int
    file_format: str
    file: str

class TrackSchemaAfterInsert(TrackSchemaBeforeInsert):
    id: int

class TrackSchema(TrackSchemaAfterInsert):
    artists_list: list[str]
    release: str

class ReleaseSchemaBeforeInsert(TunedModel):
    name: str
    genres_id_list: list[int]
    releases_types_id: int
    release_date: datetime
    artists_id_list: list[int]
    cover: Optional[str] = None
    tracks: Optional[list[TrackSchemaBeforeInsert]] = None

class ReleaseSchemaAfterInsert(ReleaseSchemaBeforeInsert):
    id: int

class TracksListSchema(TunedModel):
    id: int
    title: str
    number: int
    duration: str
    bitrate: int
    file_size: Decimal
    file_format: str
    file: str

class ReleaseSchema(TunedModel):
    id: int
    release_type: str
    title: str
    release_date: str
    genres: list[str]
    artists: list[str]
    cover: str
    tracks: Optional[list[TracksListSchema]] = None
