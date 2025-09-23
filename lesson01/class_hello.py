from progress.bar import Bar
import time


class Introduction(object):
    def __init__(self, time):
        self._range = 20
        self._time = time
        self._bar = Bar("Generating hello", max=self._range)
        self.final_message = "ERROR: No message generated"
        print("Starting introduction...")

    def run(self):
        for _ in range(self._range):
            # Simulate work being done
            time.sleep(self._time / self._range)
            self._bar.next()
        self._bar.finish()
        self.final_message = "Hello, world!"

    def print_message(self):
        print(self.final_message)


if __name__ == "__main__":
    start_t = time.time()
    intro = Introduction(10)
    intro.run()
    intro.print_message()
    end_t = time.time()
    print(f"Execution time: {end_t - start_t} seconds")
