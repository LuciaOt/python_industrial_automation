# -------------------------------
# Better timing control
# -------------------------------
import time

interval = 0.1  # expected loop time (100 ms)
iterations = 20
print("Let's try to have a better timing control...\n")
print("Target interval per loop:", interval * 1000, "ms\n")

start_time = time.time()

for i in range(iterations):
    loop_start = time.time()
    # Do some "work" by creating and destroying objects
    data = [j for j in range(10000)]  # create a list of 10k ints
    squared = [x * x for x in data]  # process them
    del data, squared  # free memory (triggers GC eventually)

    loop_end = time.time()
    work_time = loop_end - loop_start

    time.sleep(max(0, interval - work_time))
    actual = time.time() - loop_start
    print(
        f"Loop {i+1:02d}: actual={actual*1000:.1f}ms "
        f"(expected {interval*1000:.1f}ms, ",
        f"drift {(actual - interval)*1000:+.1f}ms)",
    )

end_time = time.time()
total_time = end_time - start_time
print(
    f"\nTotal time for {iterations} iterations: {total_time*1000:.1f} ms. "
    f"Expected: {(iterations * interval * 1000):.1f} ms."
)
