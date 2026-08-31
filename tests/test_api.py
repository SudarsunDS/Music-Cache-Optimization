from fastapi.testclient import TestClient

from app.main import app, song_cache


client = TestClient(app)


def setup_function():

    song_cache.clear()


def test_song_cache_miss_then_hit():

    first_request = client.get("/songs/1")

    second_request = client.get("/songs/1")


    assert first_request.status_code == 200

    assert first_request.json()["source"] == "database"


    assert second_request.status_code == 200

    assert second_request.json()["source"] == "cache"


def test_cache_stats():

    client.get("/songs/1")

    client.get("/songs/1")


    response = client.get("/cache/stats")


    assert response.status_code == 200

    assert response.json()["hits"] >= 1
