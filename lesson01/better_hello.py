from progress.bar import Bar
import time

start_t = time.time()
bar = Bar("Generating hello", max=20)
for i in range(20):
    # Simulate work being done
    time.sleep(0.25)
    bar.next()
bar.finish()
print("Hello, world!")

end_t = time.time()
print(f"Execution time: {end_t - start_t} seconds")
