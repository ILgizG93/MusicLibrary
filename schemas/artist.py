from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ArtistSchemaBeforeAppend(TunedModel):
    name: str
    countries_id: int
    origin_date: Optional[datetime] = None
    is_group: Optional[bool] = None
    description: Optional[str] = None

class ArtistSchemaAfterAppend(TunedModel):
    id: int
    name: str
    origin_date: Optional[datetime] = None
    is_group: Optional[bool] = None
    description: Optional[str] = None

class ArtistSchema(ArtistSchemaAfterAppend):
    country: str
