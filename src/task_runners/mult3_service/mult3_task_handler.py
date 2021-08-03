from src.common import constants
from src.common.databases_struct import job_events
from src.task_runners.base_queue_handler import BaseQueueHandler


class Mult3TaskHandler(BaseQueueHandler):
    def __init__(self, logger, data_provider):
        super().__init__(logger, data_provider, constants.task_name_mult3)

    def get_result(self, params: dict) -> int:
        return params[constants.key_param_first] * params[constants.key_param_second] * params[
            constants.key_param_third]
