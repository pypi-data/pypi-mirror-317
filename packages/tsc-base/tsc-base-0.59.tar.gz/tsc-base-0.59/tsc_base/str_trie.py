# Description: 实现一个 StrTrie 类，继承自 datrie.Trie 类，支持字符串作为 key，datrie==0.8.2

import string
import datrie
from typing import Generator, Optional, Generic, TypeVar
import threading


V = TypeVar('V')


class StrTrie(datrie.Trie, Generic[V]):
    """
    支持线程安全的 Trie，适用于同步和协程混合场景。
    """
    def __init__(self):
        super().__init__(string.hexdigits)
        self._lock = threading.RLock()

    def _thread_safe(func):
        """线程安全装饰器"""
        def wrapper(self, *args, **kwargs):
            with self._lock:  # 使用线程锁确保同步和协程安全
                return func(self, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def _str_to_hex(s: str):
        return s.encode('utf-8').hex()
    
    @staticmethod
    def _hex_to_str(h: str):
        return bytes.fromhex(h).decode('utf-8')
    
    @_thread_safe
    def __getitem__(self, key: str):
        return super().__getitem__(self._str_to_hex(key))

    @_thread_safe
    def __setitem__(self, key: str, value: V):
        super().__setitem__(self._str_to_hex(key), value)
    
    @_thread_safe
    def __contains__(self, key: str):
        return super().__contains__(self._str_to_hex(key))
    
    @_thread_safe
    def __delitem__(self, key: str):
        super().__delitem__(self._str_to_hex(key))
    
    @_thread_safe
    def __iter__(self):
        return (self._hex_to_str(k) for k in super().__iter__())
    
    @_thread_safe
    def setdefault(self, key: str, default: V):
        return super().setdefault(self._str_to_hex(key), default)
    
    @_thread_safe
    def prefixes(self, key: str) -> list[str]:
        """返回所有可以作为传入 key 前缀的内部 key"""
        return [self._hex_to_str(p) for p in super().prefixes(self._str_to_hex(key))]
    
    @_thread_safe
    def prefix_items(self, key: str) -> list[tuple[str, V]]:
        return [(self._hex_to_str(p[0]), p[1]) for p in super().prefix_items(self._str_to_hex(key))]
    
    @_thread_safe
    def prefix_values(self, key: str) -> list[V]:
        return [v for v in super().prefix_values(self._str_to_hex(key))]
    
    @_thread_safe
    def iter_prefixes(self, key: str) -> Generator[str, None, None]:
        for p in super().iter_prefixes(self._str_to_hex(key)):
            yield self._hex_to_str(p)
    
    @_thread_safe
    def iter_prefix_items(self, key: str) -> Generator[tuple[str, V], None, None]:
        for p in super().iter_prefix_items(self._str_to_hex(key)):
            yield (self._hex_to_str(p[0]), p[1])
    
    @_thread_safe
    def iter_prefix_values(self, key: str) -> Generator[V, None, None]:
        for v in super().iter_prefix_values(self._str_to_hex(key)):
            yield v
    
    @_thread_safe
    def has_keys_with_prefix(self, prefix: str) -> bool:
        return super().has_keys_with_prefix(self._str_to_hex(prefix))
    
    @_thread_safe
    def keys(self, prefix: Optional[str] = None) -> list[str]:
        """返回所有以 prefix 为前缀的 key"""
        if prefix is None:
            return [self._hex_to_str(k) for k in super().keys()]
        return [self._hex_to_str(k) for k in super().keys(self._str_to_hex(prefix))]
    
    @_thread_safe
    def items(self, prefix: Optional[str] = None) -> list[tuple[str, V]]:
        if prefix is None:
            return [(self._hex_to_str(k), v) for k, v in super().items()]
        return [(self._hex_to_str(k), v) for k, v in super().items(self._str_to_hex(prefix))]
    
    @_thread_safe
    def values(self, prefix: Optional[str] = None) -> list[V]:
        if prefix is None:
            return super().values()
        return [v for v in super().values(self._str_to_hex(prefix))]
    
    @_thread_safe
    def get(self, key: Optional[str], default: V = None) -> V:
        if key is None:
            return default
        return super().get(self._str_to_hex(key), default)
    
    @_thread_safe
    def pop(self, key: Optional[str], default: V = None) -> V:
        if key is None:
            return default
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default
    
    @_thread_safe
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
    
    @_thread_safe
    def longest_prefix(self, key: str, default=datrie.RAISE_KEY_ERROR) -> str:
        p = super().longest_prefix(self._str_to_hex(key), default)
        if p is default:
            return p
        return self._hex_to_str(p)
    
    @_thread_safe
    def longest_prefix_item(self, key: str, default=datrie.RAISE_KEY_ERROR) -> tuple[str, V]:
        p = super().longest_prefix_item(self._str_to_hex(key), default)
        if p is default:
            return p
        return (self._hex_to_str(p[0]), p[1])
    
    @_thread_safe
    def longest_prefix_value(self, key: str, default=datrie.RAISE_KEY_ERROR) -> V:
        return super().longest_prefix_value(self._str_to_hex(key), default)


import unittest

# 假设 StrTrie 类已经正确导入

class TestStrTrie(unittest.TestCase):
    
    def setUp(self):
        # 创建一个 StrTrie 实例
        self.trie: StrTrie[str] = StrTrie()
    
    def test_setitem_and_getitem(self):
        # 测试 __setitem__ 和 __getitem__
        self.trie["hello"] = "world"
        self.assertEqual(self.trie["hello"], "world")
    
    def test_contains(self):
        # 测试 __contains__
        self.trie["key"] = "value"
        self.assertTrue("key" in self.trie)
        self.assertFalse("missing_key" in self.trie)
    
    def test_delitem(self):
        # 测试 __delitem__
        self.trie["to_delete"] = "value"
        del self.trie["to_delete"]
        self.assertNotIn("to_delete", self.trie)
    
    def test_update(self):
        # 测试 update 方法
        self.trie.update({"foo": "bar", "baz": "qux"})
        print("Trie items after update:", list(self.trie.items()))  # 调试打印
        self.assertEqual(self.trie["foo"], "bar")
        self.assertEqual(self.trie["baz"], "qux")
    
    def test_setdefault(self):
        # 测试 setdefault
        result = self.trie.setdefault("new_key", "default_value")
        self.assertEqual(result, "default_value")
        self.assertEqual(self.trie["new_key"], "default_value")
    
    def test_prefixes(self):
        # 测试 prefixes
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertEqual(self.trie.prefixes("ap"), [])
    
    def test_prefix_items(self):
        # 测试 prefix_items
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertEqual(self.trie.prefix_items("apple你好空"), [("apple", "fruit")])
    
    def test_prefix_values(self):
        # 测试 prefix_values
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertEqual(self.trie.prefix_values("apricot23"), ["fruit"])
    
    def test_iter_prefixes(self):
        # 测试 iter_prefixes
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        result = list(self.trie.iter_prefixes("bananaabc"))
        self.assertEqual(result, ["banana"])
    
    def test_iter_prefix_items(self):
        # 测试 iter_prefix_items
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        result = list(self.trie.iter_prefix_items("ap"))
        self.assertEqual(result, [])
    
    def test_iter_prefix_values(self):
        # 测试 iter_prefix_values
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        result = list(self.trie.iter_prefix_values("ap"))
        self.assertEqual(result, [])
    
    def test_has_keys_with_prefix(self):
        # 测试 has_keys_with_prefix
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertTrue(self.trie.has_keys_with_prefix("ap"))
        self.assertFalse(self.trie.has_keys_with_prefix("ba1"))
    
    def test_keys(self):
        # 测试 keys
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertEqual(self.trie.keys(), ["apple", "apricot", "banana"])
        self.assertEqual(self.trie.keys("ap"), ["apple", "apricot"])
    
    def test_items(self):
        # 测试 items
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertEqual(self.trie.items(), [("apple", "fruit"), ("apricot", "fruit"), ("banana", "fruit")])
        self.assertEqual(self.trie.items("ap"), [("apple", "fruit"), ("apricot", "fruit")])
    
    def test_values(self):
        # 测试 values
        self.trie["apple"] = "fruit"
        self.trie["apricot"] = "fruit"
        self.trie["banana"] = "fruit"
        self.assertEqual(self.trie.values(), ["fruit", "fruit", "fruit"])
        self.assertEqual(self.trie.values("ap"), ["fruit", "fruit"])
    
    def test_get(self):
        # 测试 get
        self.trie["apple"] = "fruit"
        self.assertEqual(self.trie.get("apple"), "fruit")
        self.assertEqual(self.trie.get("missing", "default"), "default")
    
    def test_pop(self):
        # 测试 pop
        self.trie["apple"] = "fruit"
        print("Trie before pop:", list(self.trie.items()))  # 调试打印
        self.assertEqual(self.trie["apple"], "fruit")
        result = self.trie.pop("apple")
        print("Trie after pop:", list(self.trie.items()))  # 调试打印
        self.assertEqual(result, "fruit")
        self.assertNotIn("apple", self.trie)
        self.assertEqual(self.trie.pop("missing", "default"), "default")
    
    def test_longest_prefix(self):
        # 测试 longest_prefix
        self.trie["abc/123/abc/"] = "1"
        self.trie["abc/123/"] = "2"
        self.trie["abc/"] = "3"
        self.trie["banana"] = "4"
        self.trie["banana123"] = "5"
        self.assertEqual(self.trie.longest_prefix("abc/"), "abc/")
        self.assertEqual(self.trie.longest_prefix("abc/123/abc/fire"), "abc/123/abc/")
        self.assertEqual(self.trie.longest_prefix("banana2334"), "banana")
        self.assertEqual(self.trie.longest_prefix("missing", ""), "")
    
    def test_longest_prefix_item(self):
        # 测试 longest_prefix_item
        self.trie["abc/123/abc/"] = "1"
        self.trie["abc/123/"] = "2"
        self.trie["abc/"] = "3"
        self.trie["banana"] = "4"
        self.trie["banana123"] = "5"
        self.assertEqual(self.trie.longest_prefix_item("abc/"), ("abc/", "3"))
        self.assertEqual(self.trie.longest_prefix_item("abc/123/abc/fire"), ("abc/123/abc/", "1"))
        self.assertEqual(self.trie.longest_prefix_item("banana2334"), ("banana", "4"))
        self.assertEqual(self.trie.longest_prefix_item("missing", ("", "")), ("", ""))
    
    def test_longest_prefix_value(self):
        # 测试 longest_prefix_value
        self.trie["abc/123/abc/"] = "1"
        self.trie["abc/123/"] = "2"
        self.trie["abc/"] = "3"
        self.trie["banana"] = "4"
        self.trie["banana123"] = "5"
        self.assertEqual(self.trie.longest_prefix_value("abc/"), "3")
        self.assertEqual(self.trie.longest_prefix_value("abc/123/abc/fire"), "1")
        self.assertEqual(self.trie.longest_prefix_value("banana2334"), "4")
        self.assertEqual(self.trie.longest_prefix_value("missing", ""), "")


if __name__ == "__main__":
    unittest.main()
