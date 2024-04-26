from django.core.cache import cache


class SimpleCache:
    DEFAULT_TIMEOUT = 60 * 60 * 24  # 24 hrs

    @classmethod
    def set(cls, key, value, timeout=DEFAULT_TIMEOUT):
        """
        Create or update a cache entry with the given value.
        """
        cache.set(key, value, timeout=timeout)

    @classmethod
    def get(cls, key):
        """
        Retrieve the value of the cache entry, or None if the entry does not exist.
        """
        return cache.get(key)
