# FEEL FREE TO ADD MORE FUNCTIONS AS PER YOUR NEED
# THERE IS NO UNCHANGEABLE "MAIN" FUNCTION IN THIS HW

import time
import random

_EMPTY   = object()   # slot has never been occupied
_DELETED = object()   # slot held an entry that was deleted (tombstone)

# Implement HashMap in this class
# Do not use built in dictionary
# Implement own hashing function using division/multiplication method
class HashMap:
    LOAD_THRESHOLD = 0.5           # resize when α exceeds this
    _A = (5 ** 0.5 - 1) / 2 

    def __init__(self, size=101, hash_method = "division"):
        self._size        = size
        self._count       = 0          # live key-value pairs
        self._hash_method = hash_method
        # 2 parallel arrays-> for keys and values. Every slot starts empty.
        self._keys   = [_EMPTY] * self._size
        self._values = [_EMPTY] * self._size

    # retrieve a value associated with the key
    def search(self,key):
        index = self._probe(key)
        if index is None:
            return None
        return self._values[index]

    def search_with_probes(self, key):
        # returns probe count as (value, probes)
        index, probes = self._probe(key, count_probes=True)
        value = self._values[index] if index is not None else None
        return value, probes

    # insert the key value pair into the hash tables
    def insert(self,key,value):
        if (self._count + 1) / self._size > self.LOAD_THRESHOLD:
            self.dynamicResizing()
 
        start     = self._hash(key, self._hash_method)
        tombstone = None   # helps remember first tombstone
 
        for i in range(self._size):
            idx  = (start + i) % self._size
            slot = self._keys[idx]
 
            if slot is _EMPTY:
                # Use tombstone slot if we passed one, otherwise use this slot
                target = tombstone if tombstone is not None else idx
                self._keys[target]   = key
                self._values[target] = value
                self._count += 1
                return
 
            elif slot is _DELETED:
                if tombstone is None:
                    tombstone = idx   # to remember but keep probing 
 
            elif slot == key:
                self._values[idx] = value   # updatinge existing key
                return
 
        # table full exception handling
        if tombstone is not None:
            self._keys[tombstone]   = key
            self._values[tombstone] = value
            self._count += 1
 
    def insert_with_probes(self, key, value):
            if (self._count + 1) / self._size > self.LOAD_THRESHOLD:
                self.dynamicResizing()
            start     = self._hash(key, self._hash_method)
            tombstone = None
            probes    = 0
            for i in range(self._size):
                probes += 1
                idx  = (start + i) % self._size
                slot = self._keys[idx]
                if slot is _EMPTY:
                    target = tombstone if tombstone is not None else idx
                    self._keys[target]   = key
                    self._values[target] = value
                    self._count += 1
                    return probes
                elif slot is _DELETED:
                    if tombstone is None:
                        tombstone = idx
                elif slot == key:
                    self._values[idx] = value
                    return probes
            if tombstone is not None:
                self._keys[tombstone]   = key
                self._values[tombstone] = value
                self._count += 1
            return probes

    # remove the key value pair from the hash table
    def delete(self,key):
        index = self._probe(key)
        if index is None:
            return False
        self._keys[index]   = _DELETED   # tombstone retains probe chains 
        self._values[index] = _DELETED
        self._count -= 1
        return True

    # optional for open addressing collision method
    # if you choose chaining, don't forget to discuss it in the report
    def dynamicResizing(self):
        new_size   = self._next_prime(2 * self._size)
        old_keys   = self._keys
        old_values = self._values
 
        self._size   = new_size
        self._count  = 0
        self._keys   = [_EMPTY] * new_size
        self._values = [_EMPTY] * new_size
 
        for k, v in zip(old_keys, old_values):
            if k is not _EMPTY and k is not _DELETED:
                self.insert(k, v)

    # hashing methods
    def _hash(self, key, method="division"):
        return self._hash_with_size(key, method, self._size)

    def _hash_with_size(self, key, method, size):
        if isinstance(key, str):
            k = 0
            for ch in key:
                k = k * 31 + ord(ch)
        else:
            k = int(key)
 
        k = abs(k)
 
        if method == "division":
            return k % size
 
        elif method == "multiplication":
            fractional = (k * self._A) % 1.0
            return int(size * fractional)
 
        else:
            raise ValueError(f"Unknown hash method: '{method}'. ","\nUse 'division' or 'multiplication'.")


    def _probe(self, key, count_probes=False):
        start  = self._hash(key, self._hash_method)
        probes = 0
        for i in range(self._size):
            probes += 1
            idx  = (start + i) % self._size
            slot = self._keys[idx]
 
            if slot is _EMPTY:
                return (None, probes) if count_probes else None
            elif slot is not _DELETED and slot == key:
                return (idx, probes) if count_probes else idx
 
        return (None, probes) if count_probes else None
 
    @staticmethod
    def _is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
 
    @staticmethod
    def _next_prime(n):
        # returns the smallest prime that is >= n
        candidate = n if n % 2 != 0 else n + 1
        while not HashMap._is_prime(candidate):
            candidate += 2
        return candidate
  
    def load_factor(self):
        return self._count / self._size
 
    def __len__(self):
        return self._count
 
    def __repr__(self):
        return (f"HashMap(size={self._size}, count={self._count}, "
                f"load={self.load_factor():.3f}, method='{self._hash_method}')")
    
# Problem 2: Performance Analysis

def generate_keys(distribution, n):
    # uniform, skewed, or sequential
    if distribution == "uniform":
        return [random.randint(0, 10 * n) for _ in range(n)]
    elif distribution == "skewed":
        keys = []
        for _ in range(n):
            if random.random() < 0.8:
                keys.append(random.randint(0, 100))
            else:
                keys.append(random.randint(0, 10 * n))
        return keys
    elif distribution == "sequential":
        return list(range(n))
    else:
        raise ValueError(f"Unknown distribution: '{distribution}'. ","\nUse 'uniform', 'skewed', or 'sequential'.")

def measure_search_time(hashmap, keys):
    # use time.perf_counter()
    times = []
    for k in keys:
        t0 = time.perf_counter()
        hashmap.search(k)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)

def experiment_load_factor_vs_time():
    TABLE_SIZES  = [503, 1009, 5003]       # taking three fixed prime sizes for table
    LOAD_STEPS   = [0.1, 0.2, 0.3, 0.4, 0.45]
    SAMPLE_SIZE  = 200                     # sampled per timing unit
    HASH_METHODS = ["division", "multiplication"]
 
    print("EXPERIMENT 1: Load Factor vs. Average Search Time")
    hdr = (f"{'Method':<16} {'TableSize':>10} {'LoadFactor':>11} "
           f"{'SuccAvg(µs)':>13} {'FailAvg(µs)':>13}")
    print(hdr)
    print("\n\n")
 
    for method in HASH_METHODS:
        for size in TABLE_SIZES:
            # builds a pool of keys big enough to reach max load step
            max_keys = int(LOAD_STEPS[-1] * size) + 10
            all_keys = list(range(max_keys * 3))      # sequential pooling
            random.shuffle(all_keys)
            inserted = []
            hm = HashMap(size=size, hash_method=method)
 
            step_idx = 0
            for key in all_keys:
                if step_idx >= len(LOAD_STEPS):
                    break
                hm.insert(key, key)
                inserted.append(key)
 
                target_load = LOAD_STEPS[step_idx]
                if hm.load_factor() >= target_load - 0.005:
                    sample_hit  = random.sample(inserted, min(SAMPLE_SIZE, len(inserted)))
                    avg_success = measure_search_time(hm, sample_hit) * 1e6   
 
                    fail_start  = max_keys * 3 + 1
                    sample_miss = list(range(fail_start, fail_start + SAMPLE_SIZE))
                    avg_fail    = measure_search_time(hm, sample_miss) * 1e6  
 
                    print(f"{method:<16} {size:>10} {hm.load_factor():>11.3f} "
                          f"{avg_success:>13.4f} {avg_fail:>13.4f}")
                    step_idx += 1
 
        print()

def experiment_key_distribution():
    TABLE_SIZE   = 1009
    TARGET_LOAD  = 0.4
    N_KEYS       = int(TABLE_SIZE * TARGET_LOAD)
    DISTRIBUTIONS = ["uniform", "skewed", "sequential"]
    HASH_METHODS  = ["division", "multiplication"]
    SAMPLE_SIZE   = 200
 
    print("EXPERIMENT 2: Key Distribution Comparisons  "
          f"(table_size={TABLE_SIZE}, target_load≈{TARGET_LOAD})")
 
    print("\n\nPart A: Average Search Time by Distribution\n\n")
    hdr = (f"{'Method':<16} {'Distribution':<14} {'ActualLoad':>11} "
           f"{'SuccAvg(µs)':>13} {'FailAvg(µs)':>13}")
    print(hdr)
    print("\n\n")
 
    for method in HASH_METHODS:
        for dist in DISTRIBUTIONS:
            keys = generate_keys(dist, N_KEYS)
            hm   = HashMap(size=TABLE_SIZE, hash_method=method)
            for k in keys:
                hm.insert(k, k)
 
            sample_hit  = random.sample(keys, min(SAMPLE_SIZE, len(keys)))
            avg_success = measure_search_time(hm, sample_hit) * 1e6
 
            fail_base   = max(keys) + 1000 if keys else 10_000
            sample_miss = list(range(fail_base, fail_base + SAMPLE_SIZE))
            avg_fail    = measure_search_time(hm, sample_miss) * 1e6
 
            print(f"{method:<16} {dist:<14} {hm.load_factor():>11.3f} "
                  f"{avg_success:>13.4f} {avg_fail:>13.4f}")
        print()

    # memory overhead
    print("\n\nPart B: Average Probe Length (Open Addressing Memory Overhead)\n\n")
    hdr2 = (f"{'Method':<16} {'Distribution':<14} "
            f"{'AvgInsertProbes':>16} {'AvgSearchHitProbes':>19} "
            f"{'AvgSearchMissProbes':>20}")
    print(hdr2)
    print("\n\n")
 
    for method in HASH_METHODS:
        for dist in DISTRIBUTIONS:
            keys = generate_keys(dist, N_KEYS)
            hm   = HashMap(size=TABLE_SIZE, hash_method=method)
 
            # measures insertion probe lengths
            insert_probes = []
            for k in keys:
                p = hm.insert_with_probes(k, k)
                insert_probes.append(p)
 
            # meeasures (successful)search probe lengths
            sample_hit   = random.sample(keys, min(SAMPLE_SIZE, len(keys)))
            search_hit_p = [hm.search_with_probes(k)[1] for k in sample_hit]
 
            # measures (unsuccessful) search probe lengths
            fail_base    = max(keys) + 1000 if keys else 10_000
            sample_miss  = list(range(fail_base, fail_base + SAMPLE_SIZE))
            search_miss_p = [hm.search_with_probes(k)[1] for k in sample_miss]
 
            avg_ins  = sum(insert_probes)   / len(insert_probes)
            avg_hit  = sum(search_hit_p)    / len(search_hit_p)
            avg_miss = sum(search_miss_p)   / len(search_miss_p)
 
            print(f"{method:<16} {dist:<14} "
                  f"{avg_ins:>16.3f} {avg_hit:>19.3f} {avg_miss:>20.3f}")
        print()
 

def run_experiments():
    # tests across different table sizes and load factors
    experiment_load_factor_vs_time()
    experiment_key_distribution()

if __name__ == "__main__":
    print("Basic functionality test")
    hm = HashMap(size=11)
 
    hm.insert("apple",  1)
    hm.insert("banana", 2)
    hm.insert("cherry", 3)
    hm.insert(42,       99)
 
    print("apple  →", hm.search("apple"))
    print("banana →", hm.search("banana"))
    print("cherry →", hm.search("cherry"))
    print("42     →", hm.search(42))      
    print("missing→", hm.search("missing"))
 
    # updating existing key and then looking up updated value
    hm.insert("apple", 100)
    print("apple (updated) →", hm.search("apple")) 
 
    # deleting and confirming tombstone doesnt break further probes
    hm.delete("banana")
    print("banana (deleted)→", hm.search("banana")) 
    print("cherry after delete →", hm.search("cherry"))
 
    print(hm)
 
    print("\n\nDynamic resizing test")
    hm2 = HashMap(size=5)
    for i in range(20):
        hm2.insert(i, i ** 2)
    print(f"After 20 inserts: {hm2}")
    print("key 7 →", hm2.search(7))
 
    print("\n\nMultiplication method test")
    hm3 = HashMap(size=11, hash_method="multiplication")
    for i in range(10):
        hm3.insert(i * 10, i)
    for i in range(10):
        print(f"  key {i*10:3d} → {hm3.search(i*10)}")
    print(hm3)
    
    run_experiments()


    
