from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class MemberSchemaBeforeInsert(TunedModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    stage_name: Optional[str] = None
    countries_id: int
    born_datetime: Optional[datetime] = None

class MemberSchemaAfterInsert(TunedModel):
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    stage_name: Optional[str] = None
    born_datetime: Optional[datetime] = None

class MemberSchema(MemberSchemaAfterInsert):
    born_datetime: Optional[str] = None
    full_age: Optional[int] = None
    country: str
    member_since: Optional[str] = None
    member_until: Optional[str] = None

class ArtistSchemaBeforeInsert(TunedModel):
    name: str
    countries_id: int
    origin_date: Optional[datetime] = None
    is_group: Optional[bool] = None
    description: Optional[str] = None

class ArtistSchemaAfterInsert(ArtistSchemaBeforeInsert):
    id: int

class ArtistSchema(ArtistSchemaAfterInsert):
    country: str
    members: Optional[list[MemberSchema]] = None

class ArtistTrackSchema(TunedModel):
    id: int
    title: str
    release_date: str
    number: int
    bitrate: int
    file_size: Decimal
    duration: str
    album: str
    artists: list[str]
    genres: list[str]

class ArtistReleaseSchema(TunedModel):
    id: int
    album: str
    album_type_id: int
    album_type: str
    release_date: str
    tracks_count: int
    duration: str
    size: Decimal
