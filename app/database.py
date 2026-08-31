import json

from pathlib import Path

from app.models import Song


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "songs.json"
)


def load_songs():

    with open(
        DATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        songs = json.load(file)

    return {
        song["id"]: Song(**song)
        for song in songs
    }


# Simulated in-memory database
SONG_DB = load_songs()


def get_song_from_db(song_id):

    return SONG_DB.get(song_id)


def add_song_to_db(song):

    SONG_DB[song.id] = song
