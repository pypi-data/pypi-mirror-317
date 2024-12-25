import json
import diskcache

class LocalCache:
    def __init__(self, cache_dir='.cache'):
        self.cache = diskcache.Cache(cache_dir)

    def set(self, key, value, expire=None):
        """
        Set a key-value pair in the cache with an optional expiration time.

        :param key: The key to store the value.
        :param value: The value to be stored.
        :param expire: Time in seconds after which the item expires. Defaults to None (no expiration).
        """
        if expire is not None:
            self.cache.set(key, value, expire=expire)
        else:
            self.cache.set(key, value)

    def get(self, key):
        """
        Get the value associated with the given key.

        :param key: The key to look up.
        :return: The value if the key exists, else None.
        """
        return self.cache.get(key)

    def delete(self, key):
        """
        Delete the key and its associated value from the cache.

        :param key: The key to delete.
        """
        self.cache.delete(key)

    def clear(self):
        """
        Clear all items from the cache.
        """
        self.cache.clear()

    def exists(self, key):
        """
        Check if the key exists in the cache.

        :param key: The key to check.
        :return: True if the key exists, else False.
        """
        return key in self.cache

    def __del__(self):
        self.cache.close()

    def keys(self):
        """Return an iterator over all keys in the cache."""
        return self.cache.iterkeys()

    def items_dict(self):
        """Return a dictionary of all key-value pairs in the cache."""
        ret = {}
        keys = list(self.cache.iterkeys())
        for key in keys:
            ret[key] = self.cache.get(key)
        return ret

    def to_json(self, json_path):
        dct = self.items_dict()
        with open(json_path, 'w', encoding='utf-8') as fd:
            fd.write(json.dumps(dct, ensure_ascii=False))
