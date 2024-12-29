from pyutils.scheduling import event_driven

CACHE_KEY = "cache_key"
CACHE_DATA = "cache_data"
CACHE_ITEM_KEY = "item_key"
CACHE_ITEM_VALUE = "item_value"

class CacheUpdateEvent(event_driven.Event):

    def __init__(self, cache_key=None, cache_data=None):
        if cache_key is None or cache_data is None:
            raise ValueError("cache_key and cache_data must be provided")
        super().__init__(data={
            CACHE_KEY: cache_key,
            CACHE_DATA: cache_data
        })

class CacheGetEvent(event_driven.Event):

    def __init__(self, cache_key=None):
        if cache_key is None:
            raise ValueError("cache_key must be provided")
        super().__init__(data={
            CACHE_KEY: cache_key
        })


class CacheItemUpdateEvent(event_driven.Event):

    def __init__(self, cache_key=None, item_key=None, item_value=None):
        if cache_key is None or item_key is None or item_value is None:
            raise ValueError("cache_key, item_key and item_value must be provided")
        super().__init__(data={
            CACHE_KEY: cache_key,
            CACHE_ITEM_KEY: item_key,
            CACHE_ITEM_VALUE: item_value
        })

class CacheItemGetEvent(event_driven.Event):

    def __init__(self, cache_key=None, item_key=None):
        if cache_key is None or item_key is None:
            raise ValueError("cache_key and item_key must be provided")
        super().__init__(data={
            CACHE_KEY: cache_key,
            CACHE_ITEM_KEY: item_key
        })
