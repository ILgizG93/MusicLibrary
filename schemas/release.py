from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ReleaseTypeSchema(TunedModel):
    id: int
    name: str

class TrackSchemaBeforeInsert(TunedModel):
    name: str
    artists_id_list: list[int]
    release_date: Optional[str] = None
    releases_id: Optional[int] = None
    number: Optional[int] = None
    bitrate: int
    file_size: int
    duration: int
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

class ReleaseSchemaAfterInsert(ReleaseSchemaBeforeInsert):
    id: int

class ReleaseSchema(TunedModel):
    id: int
    release_type: str
    title: str
    release_date: str
    genres: list[str]
    artists: list[str]
    cover: Optional[str] = None
