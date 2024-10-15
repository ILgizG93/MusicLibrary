from typing import Optional
import time

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select, insert, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from db.database_model import get_db_session_async
from models.models import Artist, Country, Release, ReleaseType, Track
from schemas.artist import ArtistSchema, ArtistSchemaBeforeAppend, ArtistSchemaAfterAppend

router = APIRouter()

@router.get("/", response_model=list[ArtistSchema])
async def get_artists(session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ArtistSchema]]:
    query = select(Artist.id, Artist.name, Artist.origin_date, Artist.is_group, Artist.description, Country.name.label('country')).\
            join(Country, Country.id == Artist.countries_id).\
            order_by(Artist.name.asc())
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/members")
async def get_artist_members(id: int, session: AsyncSession = Depends(get_db_session_async)):
    ...

@router.get("/{id}/releases")
async def get_artist_releases(id: int, session: AsyncSession = Depends(get_db_session_async)):
    release_date = func.to_char(Release.release_date, 'yyyy-mm-dd').label('release_date')
    query = select(
                Release.id, Release.name.label('album'), ReleaseType.name.label('album_type'), release_date,
                func.count(Track.id).over(partition_by=Release.id).label('tracks_count'),
                func.to_char((func.sum(Track.duration).over(partition_by=Release.id)*text("interval '1 sec'")), 'hh24:mi:ss').label('duration'),
                (func.sum(Track.file_size).over(partition_by=Release.id)/1024/1024).label('size')).\
            distinct().\
            join(ReleaseType, ReleaseType.id == Release.releases_types_id).\
            outerjoin(Track, Track.releases_id == Release.id).\
            where(Release.artists_id_list.contains([id])).\
            order_by(release_date.asc())
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/tracks")
async def get_artist_tracks(id: int, session: AsyncSession = Depends(get_db_session_async)):
    ...

@router.post("/append_artist", response_model=ArtistSchemaAfterAppend)
async def append_artist(body: ArtistSchemaBeforeAppend, session: AsyncSession = Depends(get_db_session_async)) -> ArtistSchemaAfterAppend:
    body: dict = body.model_dump(exclude_none=True)
    query = insert(Artist).values(**body).returning(Artist)
    data = await session.execute(query)
    result = data.scalar_one()
    await session.commit()
    return result
