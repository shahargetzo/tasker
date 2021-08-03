import json

from src.common import constants
from src.common.base_handler import BaseHandler
from src.common.databases_struct import jobs, tasks_cache, job_events


class BaseQueueHandler(BaseHandler):
    def __init__(self, logger, data_provider, task_name):
        super().__init__(logger, data_provider, task_name)
        self.job = None

    def prepare(self, message):
        params = self.job[jobs.key_task_params]
        if params:
            self.params = json.loads(params)
        self.client_name = self.job[jobs.key_client_name]

    def get_result(self, params) -> object:
        pass

    def process(self, message: dict) -> dict:
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_start_process)
        result = self.get_result(self.params)
        return {constants.key_success: True,
                constants.key_result: result}

    def validate(self, message):
        self.rid = message[constants.key_rid]
        self.job = jobs.get_job_by_rid(self.data_provider, self.rid)
        if not self.job:
            raise Exception(f'no job found for rid {self.rid}')

    def finish(self, result):
        task_result = result.get(constants.key_result)
        if task_result:
            jobs.update_job(self.data_provider, self.rid, jobs.status_done, result, jobs.result_source_tasker)
            job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_process)
            self.logger.info(f'inserting result to cache for rid {self.rid}')
            tasks_cache.insert_task(self.data_provider, self.client_name, self.task_name, self.params, task_result)

    def on_validate_failure(self, param):
        jobs.update_job(self.data_provider, self.rid, jobs.status_error, None, None)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_error_process_validation)

    def on_process_failure(self, param):
        jobs.update_job(self.data_provider, self.rid, jobs.status_error, None, None)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_error_process)
