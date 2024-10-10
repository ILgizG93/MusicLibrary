from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, text, BOOLEAN
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from db.database_model import db, db_model

###-----------------------Main Menu List------------------------###
class Menu(db_model):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    lvl: Mapped[int] = mapped_column(Integer, server_default=text("1"))
    parent: Mapped[int] = mapped_column(Integer, nullable=True)
    link: Mapped[str] = mapped_column(String(60))
    
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###


###--------------------------Countries--------------------------###
class Country(db_model):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    
    members = relationship('Member', back_populates='countries',)
    artists = relationship('Artist', back_populates='countries',)
    
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
    
    users = relationship('User', back_populates='users_groups',)
    
    __table_args__ = {"schema": db.schema}

class User(db_model):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    login: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))
    users_groups_id: Mapped[int] = mapped_column(Integer, ForeignKey(User_group.id))
    privilege_list: Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    registration_datetime: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=text("timezone('utc', now())"))
    is_deleted: Mapped[bool] = mapped_column(BOOLEAN, nullable=True)
    
    users_groups = relationship('User_group', back_populates='users',)
    
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###


###----------------------Artists & Groups-----------------------###
class Member(db_model):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(25))
    first_name: Mapped[str] = mapped_column(String(25))
    middle_name: Mapped[str] = mapped_column(String(30), nullable=True)
    countries_id: Mapped[int] = mapped_column(Integer, ForeignKey(Country.id))
    born_datetime: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    countries = relationship('Country', back_populates='members',)
    
    __table_args__ = {"schema": db.schema}

class Artist(db_model):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    countries_id: Mapped[int] = mapped_column(Integer, ForeignKey(Country.id))
    origin_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)
    is_group: Mapped[bool] = mapped_column(BOOLEAN, nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)

    countries = relationship('Country', back_populates='artists',)
    
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

    releases = relationship('Release', back_populates='releases_types',)
    
    __table_args__ = {"schema": db.schema}

class Release(db_model):
    __tablename__ = "releases"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    genres_id_list: Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    releases_types_id: Mapped[int] = mapped_column(Integer, ForeignKey(ReleaseType.id))
    release_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)
    artists_id_list: Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    cover: Mapped[str] = mapped_column(String(100), nullable=True)

    releases_types = relationship('ReleaseType', back_populates='releases',)
    tracks = relationship('Track', back_populates='releases',)
    
    __table_args__ = {"schema": db.schema}

class Track(db_model):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    artists_id_list: Mapped[ARRAY] = mapped_column(ARRAY(Integer))
    release_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)
    releases_id: Mapped[int] = mapped_column(Integer, ForeignKey(Release.id))
    number: Mapped[int] = mapped_column(Integer, nullable=True)
    bitrate: Mapped[int] = mapped_column(Integer)
    file_size: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    file: Mapped[str] = mapped_column(String(256))

    releases = relationship('Release', back_populates='tracks',)
    
    __table_args__ = {"schema": db.schema}
###-------------------------------------------------------------###
