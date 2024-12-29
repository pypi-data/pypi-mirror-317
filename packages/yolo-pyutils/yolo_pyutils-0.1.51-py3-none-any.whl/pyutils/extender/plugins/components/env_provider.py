import pyutils.extender.framework.interface as interface
import os
import pyutils.io.file as file_util
import logging

class FileBasedEnvProvider(interface.Component):
    def __init__(self, env_file):
        self.__env_file = env_file

    def start(self):
        self.__load_env()

    def stop(self):
        pass

    def get_env(self):
        return self.__env

    def __load_env(self):
        if os.path.exists(self.__env_file):
            self.__env = file_util.load_dict(self.__env_file)
            logging.debug("loaded env={}".format(self.__env))
        else:
            logging.debug("skip loading env since env file {} does not exist!".format(self.__env_file))

    def persist_env(self):
        file_util.save_dict(self.__env_file, self.__env)
        logging.info("persisted env: {}".format(self.__env))
