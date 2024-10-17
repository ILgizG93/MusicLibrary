from typing import Optional
import time

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select, insert, func, text, and_, tablesample
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from db.database_model import get_db_session_async
from models.models import Artist, ArtistMember, Member, Country, Release, ReleaseType, Track, Genre
from schemas.release import (
    ReleaseTypeSchema, ReleaseSchema, TrackSchema
)

router = APIRouter()

@router.get("/release_types/", response_model=list[ReleaseTypeSchema])
async def get_release_types(session: AsyncSession = Depends(get_db_session_async)) -> list[ReleaseTypeSchema]:
    query = select(ReleaseType).order_by(ReleaseType.id)
    data = await session.execute(query)
    result = data.scalars().all()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/random/", response_model=list[ReleaseSchema])
async def get_releases(session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ReleaseSchema]]:
    RandomRelease = aliased(Release, tablesample(Release, func.system_rows(100)))
    query = select(
                RandomRelease.id, ReleaseType.name.label('release_type'), RandomRelease.name.label('title'),
                func.to_char(RandomRelease.release_date, 'yyyy-mm-dd').label('release_date'), 
                func.array_agg(Genre.name.distinct()).label('genres'), 
                func.array_agg(Artist.name.distinct()).label('artists'), 
                RandomRelease.cover
            ).\
            join(ReleaseType, ReleaseType.id == RandomRelease.releases_types_id).\
            join(Genre, Genre.id == func.any(RandomRelease.genres_id_list)).\
            join(Artist, Artist.id == func.any(RandomRelease.artists_id_list)).\
            group_by(RandomRelease.id, ReleaseType.id).\
            order_by(func.random()).limit(2)
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)
