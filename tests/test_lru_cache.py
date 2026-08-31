from app.lru_cache import LRUCache


def test_get_and_put():

    cache = LRUCache(capacity=2)

    cache.put(1, "Song A")

    assert cache.get(1) == "Song A"

    assert cache.stats()["hits"] == 1


def test_lru_eviction():

    cache = LRUCache(capacity=2)

    cache.put(1, "Song A")

    cache.put(2, "Song B")

    # Song 1 becomes most recently used
    cache.get(1)

    # Song 2 should be evicted
    cache.put(3, "Song C")


    assert cache.get(2) is None

    assert cache.get(1) == "Song A"

    assert cache.get(3) == "Song C"

    assert cache.stats()["evictions"] == 1


def test_cache_metrics():

    cache = LRUCache(capacity=2)

    cache.put(1, "Song A")

    cache.get(1)

    cache.get(2)


    stats = cache.stats()


    assert stats["hits"] == 1

    assert stats["misses"] == 1

    assert stats["hit_rate_percent"] == 50.0
