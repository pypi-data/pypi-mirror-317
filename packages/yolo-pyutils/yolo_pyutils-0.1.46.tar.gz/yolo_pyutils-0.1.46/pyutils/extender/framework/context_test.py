import logging
import time
import unittest
from pyutils.extender.framework.context import Context
from pyutils.scheduling.event_driven import Event, Dispatcher, Handler

logging.basicConfig(stream=None, level=logging.DEBUG,
                      format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s')

class TestContext(unittest.TestCase):

    def test_dispatch(self):
        test_handler = TestHandler()
        test_dispatcher = Dispatcher()
        test_dispatcher.register_handler(test_handler)
        test_dispatcher.start()
        context = Context(None, None, test_dispatcher)
        try:
            # test event
            event = TestEvent(sleep_time=1)
            context.sync_process_event(event, 2)
            self.assertFalse(event.is_canceled())
            self.assertIsNone(event.get_error())
            logging.info(event.get_result())

            context.sync_process_event(event, 0.5)
            self.assertTrue(event.is_canceled())
            self.assertIsNotNone(event.get_error())
            logging.info(event.get_result())
        finally:
            test_dispatcher.stop()


    def test_dispatch_nested_event(self):
        test_dispatcher = Dispatcher()
        context = Context(None, None, test_dispatcher)
        test_nested_handler = TestNestedHandler(context=context)
        test_dispatcher.register_handler(test_nested_handler)
        test_dispatcher.start()

        try:
            # test invalid event: failed to find handler for event TestEvent
            nested_event = TestNestedEvent(sleep_time=0)
            context.sync_process_event(nested_event, 1)
            self.assertTrue(nested_event.has_error())
            self.assertIsNotNone(nested_event.get_error())
            self.assertIsNone(nested_event.get_result())
            self.assertEqual(str(nested_event.get_error()),
                             '[dispatcher default] failed to find handler for event TestEvent')

            # register handler for TestEvent
            test_handler = TestHandler()
            test_dispatcher.register_handler(test_handler)

            # test invalid event: timeout
            nested_event = TestNestedEvent(sleep_time=1)
            context.sync_process_event(nested_event, 0.5)
            self.assertTrue(nested_event.has_error())
            self.assertIsNotNone(nested_event.get_error())
            self.assertIsNone(nested_event.get_result())
            self.assertTrue(str(nested_event.get_error()).startswith('canceled event TestNestedEvent, timeout=0.5'))

            # test normal event
            nested_event = TestNestedEvent(sleep_time=0)
            context.sync_process_event(nested_event, 1)
            self.assertFalse(nested_event.has_error())
            self.assertIsNone(nested_event.get_error())
            self.assertIsNotNone(nested_event.get_result())
        finally:
            test_dispatcher.stop()


class TestEvent(Event):
    def __init__(self, sleep_time):
        super().__init__(data={"sleep_time": sleep_time})

class TestHandler(Handler):

    def get_applicable_event_classes(self):
        return [TestEvent]

    def handle(self, event):
        logging.info("dispatching event: {}".format(get_event_class_path(event)))
        sleep_time = event.get_data_value("sleep_time")
        time.sleep(sleep_time)
        logging.info("dispatching event done: {}".format(get_event_class_path(event)))
        event.done(result="done")

class TestNestedEvent(Event):
    def __init__(self, sleep_time):
        super().__init__(data={"sleep_time": sleep_time})


class TestNestedHandler(Handler):

    def __init__(self, context):
        self.context = context

    def get_applicable_event_classes(self):
        return [TestNestedEvent]

    def handle(self, event):
        logging.info(f"dispatching event: {get_event_class_path(event)}")
        sub_event = TestEvent(sleep_time=event.get_data_value("sleep_time"))
        sub_event.set_called_event(event)
        self.context.dispatch(sub_event)


def get_event_class_path(event):
    event_class = type(event)
    return event_class.__module__ + "." + event_class.__qualname__


if __name__ == "__main__":
    unittest.main()