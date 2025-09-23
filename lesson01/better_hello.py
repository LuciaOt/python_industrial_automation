from progress.bar import Bar
import time

bar = Bar("Generating hello", max=20)
for i in range(20):
    # Simulate work being done
    time.sleep(0.5)
    bar.next()
bar.finish()
print("Hello, world!")
