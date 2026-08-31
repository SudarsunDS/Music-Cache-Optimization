from pydantic import BaseModel, Field


class SongCreate(BaseModel):

    id: int

    title: str = Field(min_length=1)

    artist: str = Field(min_length=1)

    album: str = Field(min_length=1)

    duration_seconds: int = Field(gt=0)


class Song(SongCreate):
    pass
