from datetime import datetime, date
from typing import List

from sqlalchemy import Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from db.database_model import db, db_model

###-----------------------Main Menu List------------------------###
class Menu(db_model):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    lvl: Mapped[int] = mapped_column(Integer, server_default=text("1"))
    parent: Mapped[int | None]
    link: Mapped[str] = mapped_column(String(60))    
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###

###--------------------------Countries--------------------------###
class Country(db_model):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    members: Mapped[List["Member"]] = relationship(back_populates='countries')
    artists: Mapped[List["Artist"]] = relationship(back_populates='countries')    
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###

###-----------------------Users & Groups------------------------###
class Privilege(db_model):
    __tablename__ = "privileges"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))    
    __table_args__ = {"schema": db.schema}

class User_group(db_model):
    __tablename__ = "users_groups"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))    
    users: Mapped[List["User"]] = relationship(back_populates='users_groups')
    __table_args__ = {"schema": db.schema}

class User(db_model):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    login: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))
    users_groups_id: Mapped[int] = mapped_column(Integer, ForeignKey(User_group.id))
    privilege_list: Mapped[list] = mapped_column(ARRAY(Integer))
    registration_datetime: Mapped[datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    is_deleted: Mapped[bool | None]
    users_groups: Mapped["User_group"] = relationship(back_populates='users')    
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###

###----------------------Artists & Groups-----------------------###
class Member(db_model):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(25))
    first_name: Mapped[str] = mapped_column(String(25))
    middle_name: Mapped[str | None] = mapped_column(String(30))
    artists_id_list: Mapped[list] = mapped_column(ARRAY(Integer))
    countries_id: Mapped[int] = mapped_column(Integer, ForeignKey(Country.id))
    born_datetime: Mapped[datetime | None]
    member_since: Mapped[datetime | None]
    member_until: Mapped[datetime | None]
    countries: Mapped["Country"] = relationship(back_populates='members')
    __table_args__ = {"schema": db.schema}

class Artist(db_model):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    countries_id: Mapped[int] = mapped_column(Integer, ForeignKey(Country.id))
    origin_date: Mapped[datetime | None]
    is_group: Mapped[bool | None]
    description: Mapped[str | None] = mapped_column(String(1024))
    countries: Mapped["Country"] = relationship(back_populates='artists')
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###

###--------------------------Releases---------------------------###
class Genre(db_model):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    __table_args__ = {"schema": db.schema}

class ReleaseType(db_model):
    __tablename__ = "releases_types"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    releases: Mapped[List["Release"]] = relationship(back_populates='releases_types')
    __table_args__ = {"schema": db.schema}

class Release(db_model):
    __tablename__ = "releases"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    genres_id_list: Mapped[list] = mapped_column(ARRAY(Integer))
    releases_types_id: Mapped[int] = mapped_column(Integer, ForeignKey(ReleaseType.id))
    release_date: Mapped[datetime]
    artists_id_list: Mapped[list] = mapped_column(ARRAY(Integer))
    cover: Mapped[str | None] = mapped_column(String(100))
    releases_types: Mapped["ReleaseType"] = relationship(back_populates='releases')
    tracks: Mapped[List["Track"]] = relationship(back_populates='releases')
    __table_args__ = {"schema": db.schema}

class Track(db_model):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    artists_id_list: Mapped[list] = mapped_column(ARRAY(Integer))
    release_date: Mapped[date | None]
    releases_id: Mapped[int] = mapped_column(Integer, ForeignKey(Release.id))
    number: Mapped[int | None]
    bitrate: Mapped[int]
    file_size: Mapped[int]
    duration: Mapped[int]
    file: Mapped[str] = mapped_column(String(256))
    releases: Mapped["Release"] = relationship(back_populates='tracks')
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###
