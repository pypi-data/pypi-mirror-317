from pyutils.extender.constants import EXIT_CODE_RUN_ARGUMENTS_ERROR
from pyutils.extender.framework import interface
import argparse
import logging


class EnvCommand(interface.Command):

    def __init__(self, key, context):
        super().__init__(key, context)
        self.__args_parser = argparse.ArgumentParser()
        self.__args_parser.add_argument('-show', help='show environment variables', action="store_true")
        self.__args_parser.add_argument('-set', help='set environment variables', nargs="*")

    def run(self, args):
        # parse arguments
        parsed_args, _ = self.__args_parser.parse_known_args(args)
        if parsed_args.show:
            return self.show()
        elif parsed_args.set:
            return self.set(parsed_args.set)
        else:
            err_msg = 'invalid args: {}\n{}'.format(args, self.__args_parser.format_help())
            return None, err_msg

    def show(self):
        env = self.context.get_env()
        output = list()
        for env_key, env_value in env.items():
            output.append("{}={}".format(env_key, env_value))
        return output, None

    def set(self, env_vars):
        try:
            self.context.parse_env_vars(env_vars)
            self.context.persist_env()
        except Exception as ex:
            logging.error(str(ex))
            exit(EXIT_CODE_RUN_ARGUMENTS_ERROR)
        return 'Done', None
