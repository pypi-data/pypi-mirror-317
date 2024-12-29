import time
from abc import ABC, abstractmethod
from collections import OrderedDict
import threading
from threading import Thread
import queue
import logging

EventInfoKeyCreateTime = "create_time"
EventInfoKeyDispatchTime = "dispatch_time"
EventInfoKeyHandleTime = "handle_time"
EventInfoKeyDoneTime = "done_time"
EventInfoKeyCallbackDoneTime = "callback_done_time"

class Dispatcher:

    def __init__(self, name="default"):
        self.__name = name
        self._mapping = dict()
        self._running = False
        self._thread = Thread(target=self.handle, args=())
        self._queue = queue.Queue()
        self._done = object()

    def start(self):
        self._running = True
        self._thread.start()
        logging.info(f"[dispatcher {self.__name}] started")

    def stop(self):
        if self._running:
            self._queue.put(self._done)
            # Wait for actual termination
            self._thread.join()
            logging.info(f"[dispatcher {self.__name}] stopped")
        else:
            logging.info(f"[dispatcher {self.__name}] skip stopping which is already stopped")

    def register_handler(self, handler):
        for event_class in handler.get_applicable_event_classes():
            self.register(event_class, handler)

    def register(self, event_class, handler):
        event_name = event_class.__name__
        if not issubclass(event_class, Event):
            raise RuntimeError("[dispatcher {self.__name}] failed to register event type {event_name}")
        if event_class not in handler.get_applicable_event_classes():
            raise RuntimeError("[dispatcher {}] unsupported event type {} for handler {}".format(
                self.__name, event_name, handler.get_name()))
        handlers = self._mapping.get(event_name)
        if handlers is None:
            handlers = OrderedDict()
            handlers[handler.get_name()] = handler
            self._mapping[event_name] = handlers
        else:
            if handlers.get(handler.get_name()):
                raise RuntimeError("[dispatcher {}] handler {} already registered for event {}".format(
                    self.__name, handler.get_name(), event_name))
            handlers[handler.get_name()] = handler
        logging.info("[dispatcher {}] registered event_class {} with {} handlers: {}".format(
            self.__name, event_name, len(handlers), list(handlers.keys())))

    def unregister(self, event_class, handler):
        event_name = event_class.__name__
        handlers = self._mapping.get(event_name)
        if handlers is not None:
            for existing_handler in handlers.values():
                if existing_handler == handler:
                    handlers.remove(existing_handler)
                    logging.info("[dispatcher {}] removed handler {} from event {}"
                                 .format(self.__name, existing_handler, event_class))

    def dispatch(self, event):
        self._queue.put(event)
        event.add_info(EventInfoKeyDispatchTime, time.time())
        if self._queue.qsize() % 100 == 0:
            logging.info("[dispatcher {}] dispatch event {}, queue size: {}".format(
                self.__name, get_event_class_path(event), self._queue.qsize()))

    def sync_process(self, event, timeout=0):
        condition = threading.Event()
        event.set_done_condition(condition)
        self.dispatch(event)
        start_time = time.time_ns()
        done = condition.wait(timeout)
        if not done:
            event.cancel(timeout=timeout, elapsed_ns=time.time_ns() - start_time)
        logging.debug(f"sync_processed event {get_event_class_path(event)}, done={done}")

    def handle(self):
        logging.info("[dispatcher {}] handle thread started!".format(self.__name))
        while self._running:
            event = self._queue.get()
            if event is self._done:
                break
            if event.is_canceled():
                logging.info("[dispatcher {}] skip canceled event {}".format(self.__name, get_event_class_path(event)))
                continue
            event_name = event.__class__.__name__
            handlers = self._mapping.get(event_name)
            if handlers is None:
                err = RuntimeError("[dispatcher {}] failed to find handler for event {}".format(
                    self.__name, event_name))
                logging.error(err)
                event.done(error=err)
                continue
            for handler in handlers.values():
                try:
                    event.add_info(EventInfoKeyHandleTime, time.time())
                    handler.handle(event)
                    event.add_info(EventInfoKeyDoneTime, time.time())
                except Exception as ex:
                    logging.error("[dispatcher {}] failed to handle event {}".format(self.__name, event_name), ex)
                    event.done(error=RuntimeError(
                        f"[dispatcher {self.__name}] failed to handle event {event_name}, err={ex}"))
            logging.debug("[dispatcher {}] processed event {}, queue size: {}".format(
                self.__name, event_name, self._queue.qsize()))
        logging.info("[dispatcher {}] handle thread stopped!!".format(self.__name))


class Event(ABC):

    def __init__(self, data=None, callback=None, event=None):
        # init callback & data
        self._data = {}
        self._callback = None
        if event:
            if event.get_data():
                self._data = event.get_data()
            if event.get_callback():
                self._callback = event.get_callback()
        if data:
            self._data = data
        if callback:
            self._callback = callback
        # init others
        self._canceled = False
        self._done_cond = None
        self._result = None
        self._error = None
        self._info = OrderedDict()
        self.add_info(EventInfoKeyCreateTime, time.time())

    def get_data_value(self, key):
        # check if self.data is Map
        if hasattr(self._data, 'get'):
            return self._data.get(key)
        raise RuntimeError("data is not a Map, actual is {}".format(type(self._data)))

    def done(self, result=None, error=None):
        if error:
            self._error = error
        if result:
            self._result = result
        if self._callback:
            self._callback(result=result, error=error)
            self.add_info(EventInfoKeyCallbackDoneTime, time.time())
        if self._done_cond:
            self._done_cond.set()

    def cancel(self, timeout, elapsed_ns):
        self._canceled = True
        self._error = f"canceled event {type(self).__name__}, timeout={timeout}, elapsed_ns={elapsed_ns}"
        #logging.warning("canceled event {}".format(type(self)))

    def add_info(self, key, value):
        self._info[key] = value

    def set_done_condition(self, done_condition):
        self._done_cond = done_condition

    def set_callback(self, callback):
        self._callback = callback

    def set_called_event(self, event):
        def callback(result, error):
            event.done(result, error)
        self._callback = callback


    def get_error(self):
        return self._error

    def get_data(self):
        return self._data

    def get_callback(self):
        return self._callback

    def get_result(self):
        return self._result

    def is_canceled(self):
        return self._canceled

    def has_error(self):
        return self._error is not None

    def get_info(self):
        return self._info

class Handler(ABC):

    def get_name(self):
        return self.__class__.__name__

    @abstractmethod
    def get_applicable_event_classes(self): pass

    @abstractmethod
    def handle(self, event): pass

def get_event_class_path(event):
    event_class = type(event)
    return event_class.__module__ + "." + event_class.__qualname__
