from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ArtistSchema(TunedModel):
    id: int
    name: str
    country: str
    origin_date: Optional[datetime] = None
    is_group: Optional[bool] = None
    description: Optional[str] = None
