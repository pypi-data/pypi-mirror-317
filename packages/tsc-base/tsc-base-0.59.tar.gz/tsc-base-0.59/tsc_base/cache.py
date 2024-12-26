from typing import Generic, Hashable, TypeVar
from collections import OrderedDict

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


class LRUCache(Generic[K, V]):
    def __init__(self, capacity: int):
        self.cache: OrderedDict[K, V] = OrderedDict()
        self.capacity = capacity

    def get(self, key: K) -> V:
        if key not in self.cache:
            raise KeyError("Cache miss")
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: K, value: V):
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value
        self.cache.move_to_end(key)

    def clear(self):
        self.cache.clear()

    def __getitem__(self, key: K) -> V:
        return self.get(key)

    def __setitem__(self, key: K, value: V):
        self.put(key, value)


if __name__ == '__main__':
    # test LRUCache
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
