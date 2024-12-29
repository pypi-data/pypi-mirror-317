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
        try:
            # test event: normal
            event = TestEvent(sleep_time=0.5).set_exec_timeout(1)
            test_dispatcher.sync_handle(event)
            self.assertFalse(event.is_canceled())
            self.assertIsNone(event.get_error())
            self.assertEqual(event.get_result(), "done")

            # test event: execute timeout
            event = TestEvent(sleep_time=1).set_exec_timeout(0.5)
            test_dispatcher.sync_handle(event)
            self.assertFalse(event.is_canceled())
            self.assertIsNotNone(event.get_error())
            logging.info(event.get_error())
            self.assertTrue(str(event.get_error()).find('execute timed out for event TestEvent') != -1)
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

def get_event_class_path(event):
    event_class = type(event)
    return event_class.__module__ + "." + event_class.__qualname__


if __name__ == "__main__":
    unittest.main()
