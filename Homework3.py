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
    pass

def measure_search_time(hashmap, keys):
    # use time.perf_counter()
    pass

def run_experiments():
    # test across different table sizes and load factors
    pass