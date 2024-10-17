from typing import Optional
import time

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select, insert, func, text, and_, tablesample
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import aggregate_order_by

from db.database_model import get_db_session_async
from models.models import Artist, ArtistMember, Member, Country, Release, ReleaseType, Track, Genre
from schemas.release import (
    ReleaseTypeSchema, ReleaseSchema, TrackSchema,
    ReleaseSchemaAfterInsert, ReleaseSchemaBeforeInsert    
)

router = APIRouter()

@router.get("/release_types", response_model=list[ReleaseTypeSchema])
async def get_release_types(session: AsyncSession = Depends(get_db_session_async)) -> list[ReleaseTypeSchema]:
    query = select(ReleaseType).order_by(ReleaseType.id)
    data = await session.execute(query)
    result = data.scalars().all()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/", response_model=list[ReleaseSchema])
async def get_release(id: int, session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ReleaseSchema]]:
    query = select(
                Release.id, ReleaseType.name.label('release_type'), Release.name.label('title'),
                func.to_char(Release.release_date, 'yyyy-mm-dd').label('release_date'), 
                func.array_agg(Genre.name.distinct()).label('genres'), 
                func.array_agg(Artist.name.distinct()).label('artists'), 
                Release.cover,
                func.array_agg(aggregate_order_by(
                    func.jsonb_build_object(
                        'id', Track.id, 'title', Track.name, 'number', Track.number, 
                        'duration', func.to_char((Track.duration*text("interval '1 sec'")), 'hh24:mi:ss'), 
                        'file_size', func.round((Track.file_size/1024/1024), 2), 'bitrate', Track.bitrate, 
                        'file_format', Track.file_format, 'file', Track.file
                    ), Track.number.asc()
                )).filter(Track.id.isnot(None)).label('tracks')
            ).\
            join(ReleaseType, ReleaseType.id == Release.releases_types_id).\
            join(Genre, Genre.id == func.any(Release.genres_id_list)).\
            join(Artist, Artist.id == func.any(Release.artists_id_list)).\
            outerjoin(Track, Track.releases_id == Release.id).\
            where(Release.id == id).\
            group_by(Release.id, ReleaseType.id).\
            order_by(Release.release_date.desc().nulls_last())
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/random", response_model=list[ReleaseSchema])
async def get_random_releases(count: int = 10, session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ReleaseSchema]]:
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
            order_by(func.random()).limit(count)
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/insert", response_model=ReleaseSchema)
async def insert_artist(body: ReleaseSchemaBeforeInsert, session: AsyncSession = Depends(get_db_session_async)) -> ReleaseSchema:
    body: dict = body.model_dump(exclude_none=True)
    tracks: list[dict] = body.pop('tracks', None)
    query = insert(Release).values(**body).returning(Release.id, Release.release_date)
    data = await session.execute(query)
    result: dict = dict(data.mappings().fetchone())

    for track in tracks or []:
        track.update({'releases_id': result.get('id'), 'release_date': result.get('release_date')})
        query = insert(Track).values(**track)
        data = await session.execute(query)

    await session.commit()

    result = (await get_release(result.get('id'), session))[0]

    return result
