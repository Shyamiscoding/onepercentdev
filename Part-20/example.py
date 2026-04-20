# import time

# SIZE = 10_000_000

# print(f"Building list and set with {SIZE:,} items...\n")
# big_list = list(range(SIZE))
# big_set  = set(range(SIZE))

# target = SIZE - 1  # worst case for list: last element

# # --- List lookup ---
# start = time.time()
# found_list = target in big_list
# list_time = time.time() - start

# # --- Set lookup ---
# start = time.time()
# found_set = target in big_set
# set_time = time.time() - start

# print(f"Target: {target:,}")
# print(f"List: found={found_list}  time={list_time:.6f}s")
# print(f"Set:  found={found_set}  time={set_time:.6f}s")
# print()

# if list_time > 0 and set_time > 0:
#     ratio = list_time / set_time
#     print(f"Set was ~{ratio:,.0f}x faster than list")
# elif set_time == 0:
#     print("Set lookup was too fast to measure — essentially instant")
# print()

# # --- Missing element (not found) ---
# missing = -1

# start = time.time()
# _ = missing in big_list
# list_miss = time.time() - start

# start = time.time()
# _ = missing in big_set
# set_miss = time.time() - start

# print(f"Missing element ({missing}):")
# print(f"List: time={list_miss:.6f}s  (scanned all {SIZE:,} items)")
# print(f"Set:  time={set_miss:.6f}s  (hash jump — instant)")

import sys

s = set()
for i in range(20):
    s.add(i)
    print(i, sys.getsizeof(s))