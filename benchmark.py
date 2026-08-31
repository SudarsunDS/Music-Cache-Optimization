import random
import time

from app.lru_cache import LRUCache
from app.database import SONG_DB


def run_benchmark(

    requests=10000,

    capacity=5,

    hot_probability=0.8

):

    cache = LRUCache(
        capacity=capacity
    )


    song_ids = list(
        SONG_DB.keys()
    )


    # Popular songs requested frequently
    hot_ids = song_ids[:3]


    start_time = time.perf_counter()


    for _ in range(requests):

        # Simulate realistic repeated access
        if random.random() < hot_probability:

            song_id = random.choice(
                hot_ids
            )

        else:

            song_id = random.choice(
                song_ids
            )


        song = cache.get(song_id)


        if song is None:

            cache.put(
                song_id,
                SONG_DB[song_id]
            )


    end_time = time.perf_counter()


    elapsed_time = (
        end_time - start_time
    ) * 1000


    stats = cache.stats()


    print("\n--- Benchmark Results ---\n")

    print(f"Requests: {requests}")

    print(f"Cache Capacity: {capacity}")

    print(
        f"Elapsed Time: "
        f"{elapsed_time:.2f} ms"
    )

    print(
        f"Average Request Time: "
        f"{elapsed_time / requests:.4f} ms"
    )

    print(f"Hits: {stats['hits']}")

    print(f"Misses: {stats['misses']}")

    print(f"Evictions: {stats['evictions']}")

    print(
        f"Hit Rate: "
        f"{stats['hit_rate_percent']}%"
    )


if __name__ == "__main__":

    run_benchmark()
