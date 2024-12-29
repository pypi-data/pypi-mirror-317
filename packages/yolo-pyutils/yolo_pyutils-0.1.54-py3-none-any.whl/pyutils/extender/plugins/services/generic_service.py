from pyutils.extender.framework import interface
import logging
from abc import abstractmethod


class GenericService(interface.Service):

    def __init__(self, key=None, context=None):
        self.key = key
        self.context = context

    def reinitialize(self, init_args):
        self.stop()
        self.__init__(**init_args)
        return self.start()

    def start(self):
        logging.info("Service {} started".format(self.key))

    def stop(self):
        logging.info("Service {} stopped".format(self.key))

    @abstractmethod
    def get_applicable_event_classes(self): pass

    @abstractmethod
    def handle(self, event): pass
