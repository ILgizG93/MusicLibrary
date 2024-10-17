from typing import Optional
import time

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select, insert, func, text, and_
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from db.database_model import get_db_session_async
from models.models import Artist, ArtistMember, Member, Country, Release, ReleaseType, Track, Genre
from schemas.artist import (
    ArtistSchema, ArtistSchemaBeforeInsert, ArtistSchemaAfterInsert, 
    MemberSchema, MemberSchemaBeforeInsert, MemberSchemaAfterInsert,
    ArtistTrackSchema, ArtistReleaseSchema
)

router = APIRouter()

@router.get("/", response_model=list[ArtistSchema])
async def get_artists(session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ArtistSchema]]:
    artist_country: Country = aliased(Country)
    member_country: Country = aliased(Country)
    query = select(
                Artist.id, Artist.name, Artist.origin_date, Artist.is_group, Artist.description, 
                Artist.countries_id, artist_country.name.label('country'),
                func.array_agg(func.jsonb_build_object(
                    'id', Member.id, 'stage_name', Member.stage_name, 'born_datetime', func.to_char(Member.born_datetime, 'yyyy-mm-dd'), 
                    'full_age', func.date_part('year', func.age(Member.born_datetime)), 'country', member_country.name, 
                    'last_name', Member.last_name, 'first_name', Member.first_name, 'middle_name', Member.middle_name, 
                    'member_since', func.to_char(ArtistMember.member_since, 'yyyy-mm-dd'), 
                    'member_until', func.to_char(ArtistMember.member_until, 'yyyy-mm-dd'))
                ).filter(Member.id.isnot(None)).over(partition_by=Artist.id).label('members')
            ).distinct().\
            join(artist_country, artist_country.id == Artist.countries_id).\
            outerjoin(ArtistMember, ArtistMember.artists_id == Artist.id).\
            outerjoin(Member, Member.id == ArtistMember.members_id).\
            outerjoin(member_country, member_country.id == Member.countries_id).\
            order_by(Artist.name.asc())
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/members/", response_model=list[MemberSchema])
async def get_artist_members(id: int, session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[MemberSchema]]:
    query = select(
                Member.id, Member.last_name, Member.first_name, Member.middle_name, Member.stage_name, 
                func.to_char(Member.born_datetime, 'yyyy-mm-dd').label('born_datetime'),
                func.date_part('year', func.age(Member.born_datetime)).label('full_age'), Country.name.label('country'), 
                func.to_char(ArtistMember.member_since, 'yyyy-mm-dd').label('member_since'), 
                func.to_char(ArtistMember.member_until, 'yyyy-mm-dd').label('member_until')
            ).\
            select_from(ArtistMember).\
            join(Member, Member.id == ArtistMember.members_id).\
            join(Country, Country.id == Member.countries_id).\
            where(ArtistMember.artists_id == id).\
            order_by(ArtistMember.member_since.nulls_last(), Member.stage_name)
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/releases/", response_model=list[ArtistReleaseSchema])
async def get_artist_releases(id: int, session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ArtistReleaseSchema]]:
    release_date = func.to_char(Release.release_date, 'yyyy-mm-dd').label('release_date')
    query = select(
                Release.id, Release.name.label('album'), ReleaseType.id.label('album_type_id'), ReleaseType.name.label('album_type'), 
                release_date, func.count(Track.id).over(partition_by=Release.id).label('tracks_count'),
                func.to_char((func.sum(Track.duration).over(partition_by=Release.id)*text("interval '1 sec'")), 'hh24:mi:ss').label('duration'),
                func.round((func.sum(Track.file_size).over(partition_by=Release.id)/1024/1024), 2).label('size')).\
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

@router.get("/{id}/tracks/", response_model=list[ArtistTrackSchema])
async def get_artist_tracks(id: int, session: AsyncSession = Depends(get_db_session_async)) -> Optional[list[ArtistTrackSchema]]:
    track_artist: Artist = aliased(Artist)
    release_artist: Artist = aliased(Artist)
    query = select(
            Track.id, Track.name.label('title'), func.to_char(Track.release_date, 'yyyy-mm-dd').label('release_date'), Track.number, 
            Track.bitrate, func.round(Track.file_size/1024/1024, 2).label('file_size'), func.to_char(Track.duration*text("interval '1 sec'"), 'mi:ss').label('duration'), 
            Release.name.label('album'), func.array_agg(track_artist.name.distinct()).label('artists'),
            func.array_agg(Genre.name.distinct()).label('genres')).\
        distinct().\
        join(track_artist, Track.artists_id_list.any(track_artist.id)).\
        join(Release, Release.id == Track.releases_id).\
        join(release_artist, Release.artists_id_list.any(release_artist.id)).\
        join(Genre, Release.genres_id_list.any(Genre.id)).\
        where(Track.artists_id_list.contains([id])).\
        group_by(Track.id, Release.id).\
        order_by(Track.name)
    data = await session.execute(query)
    result = data.mappings().fetchall()
    if result:
        return result
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/insert/", response_model=ArtistSchemaAfterInsert)
async def insert_artist(body: ArtistSchemaBeforeInsert, session: AsyncSession = Depends(get_db_session_async)) -> ArtistSchemaAfterInsert:
    body: dict = body.model_dump(exclude_none=True)
    query = insert(Artist).values(**body).returning(Artist)
    data = await session.execute(query)
    result = data.scalar_one()
    await session.commit()
    return result
