import logging
import os
from abc import ABC
from pyutils.extender.plugins.services.generic_service import GenericService
from pyutils.extender.plugins.services.events.cache_events import *
import pyutils.io.file as file_util


class CacheService(GenericService, ABC):

    def __init__(self, key=None, context=None, persist_dir=None, file_format="json"):
        super().__init__(key, context)
        self._caches = dict()
        self._persist_dir = persist_dir
        # sanity check: file_format must be json or yaml
        if file_format not in ["json", "yaml"]:
            raise ValueError("file_format must be json or yaml")
        self._load_func = file_util.load_dict if file_format == "json" else file_util.load_yaml
        self._save_func = file_util.save_dict if file_format == "json" else file_util.save_yaml
        self._file_format = file_format

    def get_applicable_event_classes(self):
        return [CacheUpdateEvent, CacheGetEvent,
                CacheItemUpdateEvent, CacheItemGetEvent]

    def handle(self, event):
        if isinstance(event, CacheUpdateEvent):
            cache_key, cache_data = event.get_data_value(CACHE_KEY), event.get_data_value(CACHE_DATA)
            self._caches[cache_key] = cache_data
            logging.info(f"cache updated: cache_key={cache_key}, cache_data={cache_data}")
            self.__save_cache(cache_key)
            event.done()
        elif isinstance(event, CacheItemUpdateEvent):
            cache_key, item_key, item_value = event.get_data_value(CACHE_KEY), event.get_data_value(
                CACHE_ITEM_KEY), event.get_data_value(CACHE_ITEM_VALUE)
            cache_data = self._caches.get(cache_key)
            if cache_data is None:
                cache_data = dict()
                self._caches[cache_key] = cache_data
            cache_data[item_key] = item_value
            logging.info(
                f"cache item updated: cache_key={cache_key}, item_key={item_key}, item_value={item_value}")
            self.__save_cache(cache_key)
            event.done()
        elif isinstance(event, CacheGetEvent):
            cache_key = event.get_data_value(CACHE_KEY)
            result = self._caches.get(cache_key)
            event.done(result)
        elif isinstance(event, CacheItemGetEvent):
            cache_key, item_key = event.get_data_value(CACHE_KEY), event.get_data_value(CACHE_ITEM_KEY)
            cache_data = self._caches.get(cache_key)
            result = None
            if cache_data:
                result = cache_data.get(item_key)
            event.done(result)
        else:
            if event:
                event.done(error=f"Unsupported event: {type(event)}")
            else:
                logging.error("got None event in CacheService")


    def start(self):
        err = self.__load_caches()
        super().start()
        return err

    def __load_caches(self) -> str:
        # search all files in persist_dir
        if os.path.exists(self._persist_dir):
            for file in os.listdir(self._persist_dir):
                if file.endswith(f".{self._file_format}"):
                    cache_key = file.split(".")[0]
                    cache_data = self._load_func(os.path.join(self._persist_dir, file))
                    self._caches[cache_key] = cache_data
            logging.debug(f"loaded {len(self._caches)} caches: {self._caches}")
        else:
            return f"persist dir \"{self._persist_dir}\" does not exist!"

    def __save_cache(self, cache_key):
        cache_data = self._caches.get(cache_key)
        if cache_data:
            file = os.path.join(self._persist_dir, f"{cache_key}.{self._file_format}")
            self._save_func(file, cache_data)
            logging.debug(f"saved cache: {cache_key}")
