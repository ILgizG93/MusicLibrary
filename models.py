import json
from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

class Artist():
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    language = Column(JSONB)

    def __str__(self):
        return json.dumps(f'"id": {self.id}')

class ReleaseType():
    __tablename__ = "release_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)

class Release():
    __tablename__ = "release"
    id = Column(Integer, primary_key=True)
    release_type_id = Column(ForeignKey(ReleaseType.id), nullable=False)
    release_date = Column(TIMESTAMP, nullable=False)
    name = Column(String(40), nullable=False)
    cover = Column(String)

class Track():
    __tablename__ = "release"
    id = Column(Integer, primary_key=True)
    release_id = Column(ForeignKey(Release.id), nullable=False)
    name = Column(String(200), nullable=False)
    duration = Column(Integer)
    file_name = Column(String(255))
    cover = Column(String)
    genre = Column(JSONB)
    guest = Column(ARRAY(String))
