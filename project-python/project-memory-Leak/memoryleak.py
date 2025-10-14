import time

# This function creates a list and continuously adds large strings to it.
def memory_leak():
    data = []
    while True:
        # Append a large object to the list, simulating memory consumption
        data.append("A" * 10**6)  # 1 MB string
        time.sleep(0.1)  # Slows down to observe the memory growth

if __name__ == "__main__":
    try:
        memory_leak()
    except MemoryError:
        print("MemoryError: Out of memory!")
