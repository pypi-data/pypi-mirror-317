import unittest
from pyutils.scheduling.event_driven import *


logging.basicConfig(stream=None, level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s: %(message)s')

class ShareEvent(Event):
    def __init__(self, data):
        super().__init__(data)


class MarketEvent(Event):
    def __init__(self, data):
        super().__init__(data)


class ShareHandler(Handler):

    def __init__(self):
        self.data = list()

    def get_applicable_event_classes(self):
        return [ShareEvent]

    def get_data(self):
        return self.data

    def handle(self, event):
        self.data.append(event.get_data())


class ShareOrMarketHandler(ShareHandler):

    def get_applicable_event_classes(self):
        return [ShareEvent, MarketEvent]

def some_function():
    return False

class TestEventDriven(unittest.TestCase):

    def test_example(self):
        result = some_function()
        self.assertTrue(result, f"Expected True, but got {result}")

    def test_dispatch(self):
        dispatcher = Dispatcher()
        share_handler = ShareHandler()
        share_or_market_handler = ShareOrMarketHandler()

        # confirm that register non-event should raise error
        with self.assertRaises(RuntimeError) as err:
            dispatcher.register(ShareHandler, share_handler)
        self.assertTrue(err.exception.args[0].find("failed to register event type") != -1)

        # confirm that register unsupported event should raise error
        with self.assertRaises(RuntimeError) as err:
            dispatcher.register(MarketEvent, share_handler)
        self.assertTrue(err.exception.args[0].find("unsupported event type") != -1)

        # register events for handlers, then start dispatcher
        dispatcher.register(ShareEvent, share_handler)
        dispatcher.register(ShareEvent, share_or_market_handler)
        dispatcher.register(MarketEvent, share_or_market_handler)


        dispatcher.start()

        result = some_function()
        logging.debug(f"some_function() returned: {result}")
        self.assertTrue(result, f"Expected True, but got {result}")

        result = some_function()
        self.assertTrue(result, f"Expected True, but got {result}")

        # dispatch two events, share event should be received by both handlers,
        # market event should only be received by share_or_market_handler.
        dispatcher.dispatch(ShareEvent("data1"))
        dispatcher.dispatch(MarketEvent("data2"))

        result = some_function()
        self.assertTrue(result, f"Expected True, but got {result}")

        # handle no-registered event, should get error
        no_registered_event = Event("no-handler")
        dispatcher.dispatch(no_registered_event)
        self.assertTrue(no_registered_event.get_result() is None,
                        msg=f"no-registered event: result should be None but got: {no_registered_event.get_result()}")
        self.assertTrue(no_registered_event.get_error() is not None,
                        msg=f"no-registered event: error should not be None but got: {no_registered_event.get_error()}")

        # stop dispatcher, and then waiting for all events to be processed
        dispatcher.stop()

        # confirm that share handler processed 1 event, another handler processed 2 events
        self.assertEqual(["data1"], share_handler.get_data())
        self.assertEqual(["data1", "data2"], share_or_market_handler.get_data())


if __name__ == '__main__':
    unittest.main()
