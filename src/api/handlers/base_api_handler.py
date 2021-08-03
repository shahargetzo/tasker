import uuid

from src.common import constants
from src.common.base_handler import BaseHandler
from src.common.databases_struct import job_events, tasks_cache
from src.common.databases_struct import jobs


class BaseAPIHandler(BaseHandler):
    def __init__(self, logger, data_provider, queue_provider, task_name: str, queue_url: str, allowed_params: list):
        super().__init__(logger, data_provider, task_name)
        self.queue_provider = queue_provider
        self.queue_url = queue_url
        self.rid = uuid.uuid4().hex
        self.allowed_params = allowed_params

    def process(self, message: dict) -> dict:
        sql_success = jobs.insert_job(self.data_provider, self.rid, self.client_name, self.task_name,
                                      self.params, message.get(constants.key_ip))
        if not sql_success:
            self.logger.error('failed to enter request to db')
            return {constants.key_success: False,
                    constants.key_error: 'internal'}
        cached_result = tasks_cache.get_result_if_exists(self.data_provider, self.task_name, self.params)
        if cached_result:
            self.handle_cached_result(cached_result)
            return {
                constants.key_success: True,
                constants.key_rid: self.rid,
                constants.key_cached: True
            }
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_api_process)
        self.client_name = message[constants.key_client_name]

        queue_success = self.queue_provider.send_to_queue(self.queue_url, {'rid': self.rid})
        if not queue_success:
            self.logger.error('failed to send request to queue')
            return {constants.key_success: False,
                    constants.key_error: 'internal'}
        job_events.insert_event(self.data_provider, self.rid, self.task_name)
        return {constants.key_success: True,
                constants.key_rid: self.rid,
                constants.key_cached: False}

    def prepare(self, message):
        self.params = message[constants.key_params]
        self.client_name = message[constants.key_client_name]

    def validate(self, message):
        assert isinstance(message.get(constants.key_client_name), str)
        params = message.get(constants.key_params)
        assert isinstance(params, dict)
        if any(p not in self.allowed_params for p in params):
            raise Exception(f'allowed params are {self.allowed_params}, got {list(params.keys())}')

    def handle_cached_result(self, cached_result):
        self.logger.info(f'got cached result for {self.rid}')
        jobs.update_job(self.data_provider, self.rid, jobs.status_done, cached_result[tasks_cache.key_result],
                        jobs.result_source_cache)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_process)

    def on_validate_failure(self, param):
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_error_api_validation)
        if not jobs.get_job_by_rid(self.data_provider, self.rid):
            self.logger.info(f'no job to update status to {jobs.status_error} for request {self.rid}')
            return
        jobs.update_job(self.data_provider, self.rid, jobs.status_error, None, None)

    def on_process_failure(self, param):
        jobs.update_job(self.data_provider, self.rid, jobs.status_error, None, None)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_error_api)
