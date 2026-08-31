from fastapi import FastAPI, HTTPException

from app.models import Song, SongCreate
from app.lru_cache import LRUCache

from app.database import (
    get_song_from_db,
    add_song_to_db,
    SONG_DB
)


app = FastAPI(

    title="Music Cache Optimization API",

    description=(
        "Spotify-inspired music metadata service "
        "using a custom O(1) LRU cache."
    ),

    version="1.0.0"
)


# Cache capacity
CACHE_CAPACITY = 5


song_cache = LRUCache(
    capacity=CACHE_CAPACITY
)


@app.get("/")
def root():

    return {

        "message": "Music Cache Optimization API",

        "docs": "/docs",

        "cache_capacity": CACHE_CAPACITY

    }


@app.get("/songs")
def list_songs():

    return {

        "songs": list(SONG_DB.values()),

        "count": len(SONG_DB)

    }


@app.get("/songs/{song_id}")
def get_song(song_id: int):

    # Check cache first
    cached_song = song_cache.get(song_id)

    if cached_song is not None:

        return {

            "source": "cache",

            "song": cached_song,

            "cache_stats": song_cache.stats()

        }


    # Cache miss → database lookup
    song = get_song_from_db(song_id)


    if song is None:

        raise HTTPException(

            status_code=404,

            detail="Song not found"

        )


    # Store result in cache
    song_cache.put(
        song_id,
        song
    )


    return {

        "source": "database",

        "song": song,

        "cache_stats": song_cache.stats()

    }


@app.post("/songs", status_code=201)
def create_song(song: SongCreate):

    if song.id in SONG_DB:

        raise HTTPException(

            status_code=409,

            detail="Song ID already exists"

        )


    new_song = Song(
        **song.model_dump()
    )


    add_song_to_db(new_song)


    return {

        "message": "Song added successfully",

        "song": new_song

    }


@app.get("/cache/stats")
def cache_stats():

    return song_cache.stats()


@app.get("/cache/keys")
def cache_keys():

    return {

        "mru_to_lru":

        song_cache.keys_mru_to_lru()

    }


@app.delete("/cache")
def clear_cache():

    song_cache.clear()


    return {

        "message": "Cache cleared",

        "cache_stats": song_cache.stats()

    }
