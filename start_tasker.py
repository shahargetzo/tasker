import os
import subprocess
import sys

from common.databases_struct.db_builder import DBBuilder
from common.tasker_logger import Logger


def start_sum2_controller():
    from task_runners.services.sum2_service.sum2_controller import Sum2Controller
    path = os.path.abspath(sys.modules[Sum2Controller.__module__].__file__)
    return subprocess.Popen(['python3', path], stdout=None, stderr=None, stdin=None)


def start_process_controller():
    from task_runners.controllers.process_controller import ProcessController
    path = os.path.abspath(sys.modules[ProcessController.__module__].__file__)
    return subprocess.Popen(['python3', path], stdout=None, stderr=None, stdin=None)


def start_api():
    path = os.path.join(os.path.realpath(__file__), 'api', 'tasker_api.py')
    return subprocess.Popen(['python3', path], stdout=None, stderr=None, stdin=None)


if __name__ == '__main__':
    logger = Logger('start')
    db_builder = DBBuilder(logger)
    db_builder.create_db_if_not_exist()
    db_builder.create_tables_if_nor_exist()
    # start_process_controller()
