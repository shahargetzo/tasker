from common import constants
from common.base_handler import BaseTaskHandler
from common.databases_struct import jobs


class BaseTaskQueueHandler(BaseTaskHandler):
    def __init__(self, logger, data_provider, task_name):
        super().__init__(logger, data_provider, task_name)
        self.job = None

    def validate(self, message):
        self.rid = message[constants.key_rid]
        self.job = jobs.get_job_by_rid(self.data_provider, self.rid)
        if not self.job:
            raise Exception(f'no job found for rid {self.rid}')
