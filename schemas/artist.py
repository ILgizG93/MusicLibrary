from datetime import datetime
from typing import Optional
from pydantic import BaseModel

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

class ArtistSchemaAfterInsert(TunedModel):
    id: int
    name: str
    origin_date: Optional[datetime] = None
    is_group: Optional[bool] = None
    description: Optional[str] = None

class ArtistSchema(ArtistSchemaAfterInsert):
    country: str
    members: Optional[list[MemberSchema]] = None
