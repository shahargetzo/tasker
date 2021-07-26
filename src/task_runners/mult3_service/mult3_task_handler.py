from src.common import constants
from src.common.databases_struct import job_events
from src.common.databases_struct import jobs
from src.task_runners.base_task_queue_handler import BaseTaskQueueHandler


class Mult3TaskHandler(BaseTaskQueueHandler):
    def __init__(self, logger, data_provider):
        super().__init__(logger, data_provider, constants.task_name_mult3)

    def process(self, message: dict) -> dict:
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_start_process)
        result = self.params[constants.key_param_first] * self.params[constants.key_param_second] * self.params[
            constants.key_param_third]
        jobs.update_job(self.data_provider, self.rid, jobs.status_done, result)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_process)
        return {constants.key_success: True}
