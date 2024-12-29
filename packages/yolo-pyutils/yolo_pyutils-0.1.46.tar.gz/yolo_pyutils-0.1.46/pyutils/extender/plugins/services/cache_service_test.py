import json
import logging
from pyutils.extender.plugins.services.cache_service import CacheService, CacheGetEvent, CacheUpdateEvent, \
    CacheItemUpdateEvent, CacheItemGetEvent
from pyfakefs.fake_filesystem_unittest import TestCase

logging.basicConfig(stream=None, level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s: %(message)s')

TEST_PERSIST_DIR="/fake_dir"
TEST_CACHE_KEY="cache1"

class TestCacheService(TestCase):

    def setUp(self):
        # setup fake filesystem
        self.setUpPyfakefs()
        # create a fake directory
        self.fs.create_dir(TEST_PERSIST_DIR)
        # create a fake cache file
        self.fs.create_file(TEST_PERSIST_DIR + f"/{TEST_CACHE_KEY}.json", contents=json.dumps({"k1": "v1", "k2": "v2"}))


    def test_cache_service(self):
        # invalid case: invalid file_format, catch ValueError
        with self.assertRaises(ValueError) as err:
            CacheService(key="test_cache_service", persist_dir=TEST_PERSIST_DIR, file_format="invalid")
        self.assertEqual(str(err.exception), "file_format must be json or yaml")

        # invalid case: got error when providing invalid persist dir
        cache_service = CacheService(key="test_cache_service", persist_dir="", context=None)
        err = cache_service.start()
        self.assertEqual(err, "persist dir \"\" does not exist!")

        # normal case
        cache_service = CacheService(key="test_cache_service", persist_dir=TEST_PERSIST_DIR, context=None)
        cache_service.start()
        cache_service.handle(None)

        # check CacheGetEvent and whether the cache is loaded
        event = CacheGetEvent(cache_key=TEST_CACHE_KEY)
        cache_service.handle(event)
        self.assertFalse(event.is_canceled())
        self.assertIsNone(event.get_error())
        self.assertEqual(event.get_result(), {"k1": "v1", "k2": "v2"})

        # check CacheUpdateEvent
        test_new_cache_key = "cache2"
        event = CacheUpdateEvent(cache_key=test_new_cache_key, cache_data={"k3": "v3"})
        cache_service.handle(event)
        self.assertFalse(event.is_canceled())
        self.assertIsNone(event.get_error())

        # check new cache updated
        event = CacheGetEvent(cache_key=test_new_cache_key)
        cache_service.handle(event)
        self.assertFalse(event.is_canceled())
        self.assertIsNone(event.get_error())
        self.assertEqual(event.get_result(), {"k3": "v3"})

        # check new cache persisted
        with open(TEST_PERSIST_DIR + f"/{test_new_cache_key}.json", "r") as f:
            self.assertEqual(json.load(f), {"k3": "v3"})

        # check CacheItemUpdateEvent
        event = CacheItemUpdateEvent(cache_key=test_new_cache_key, item_key="k3", item_value="newV")
        cache_service.handle(event)
        self.assertFalse(event.is_canceled())
        self.assertIsNone(event.get_error())

        # check CacheItemGetEvent
        event = CacheItemGetEvent(cache_key=test_new_cache_key, item_key="k3")
        cache_service.handle(event)
        self.assertFalse(event.is_canceled())
        self.assertIsNone(event.get_error())
        self.assertEqual(event.get_result(), "newV")

        # cleanup
        cache_service.stop()
