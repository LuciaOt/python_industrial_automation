# -------------------------------
# Basic timing control
# -------------------------------
import time

interval = 0.1  # expected loop time (100 ms)
iterations = 20
print("Basic timing control demo...\n")
print("Target interval per loop:", interval * 1000, "ms\n")

previous = time.time()
start_time = previous

for i in range(iterations):
    # Do some "work" by creating and destroying objects
    data = [j for j in range(10000)]  # create a list of 10k ints
    squared = [x * x for x in data]  # process them
    del data, squared  # free memory (triggers GC eventually)

    # Sleep to aim for consistent cycle time
    time.sleep(interval)

    now = time.time()
    actual = now - previous
    drift = actual - interval

    print(
        f"Loop {i+1:02d}: actual={actual*1000:.1f}ms "
        f"(expected {interval*1000:.1f}ms, drift {drift*1000:+.1f}ms)"
    )

    previous = now

end_time = time.time()
total_time = end_time - start_time
print(
    f"\nTotal time for {iterations} iterations: {total_time*1000:.1f} ms. "
    f"Expected: {(iterations * interval * 1000):.1f} ms."
)
