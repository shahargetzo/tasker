import json

from common import constants
from common.databases_struct import job_events, jobs
from task_runners.handlers.base_task_queue_handler import BaseTaskQueueHandler


class Sum2TaskHandler(BaseTaskQueueHandler):
    def __init__(self, logger, data_provider):
        super().__init__(logger, data_provider, constants.task_name_sum2)

    def process(self, message: dict) -> dict:
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_start_process)
        self.params = json.load(self.job[jobs.key_task_params])
        result = self.params['first'] + self.params['second']
        jobs.update_job(self.data_provider, self.rid, jobs.status_done, result)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_process)
        return {constants.key_success: True}
