from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database_model import get_db_session_async
from models.models import *
from schemas.schemas import *

router = APIRouter()

@router.get("/get_artist", response_model=list[ArtistSchema])
async def get_flights(session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ArtistSchema]]:
    query = select(Artist.id, Artist.name, Artist.origin_date, Artist.is_group, Artist.description, Country.name.label('country')).\
            select_from(Artist).\
            join(Country, Country.id == Artist.countries_id).\
            order_by(Artist.name.asc())
    data = await session.execute(query)
    result = data.fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)
