import random, time

def has_duplicate_slow(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]: return True
    return False

def has_duplicate_fast(nums):
    seen = set()
    for n in nums:
        if n in seen: return True
        seen.add(n)
    return False

nums = random.sample(range(10_000_000), 20_000)   # 20k unique ints — no duplicates

for name, fn in [("slow", has_duplicate_slow), ("fast", has_duplicate_fast)]:
    t = time.perf_counter()
    fn(nums)
    print(f"{name}: {(time.perf_counter() - t) * 1000:.1f} ms")

# Expected output on a laptop (numbers vary by machine, ratio doesn't):
# slow: ~1000-3000 ms
# fast: ~1 ms
# → same input, same answer, ~1,000× time difference