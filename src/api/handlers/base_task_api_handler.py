import uuid

from src.common import constants
from src.common.base_handler import BaseTaskHandler
from src.common.databases_struct import job_events
from src.common.databases_struct import jobs


class BaseTaskAPIHandler(BaseTaskHandler):
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
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_api_process)
        self.client_name = message[constants.key_client_name]

        queue_success = self.queue_provider.send_to_queue(self.queue_url, {'rid': self.rid})
        if not queue_success:
            self.logger.error('failed to send request to queue')
            return {constants.key_success: False,
                    constants.key_error: 'internal'}
        job_events.insert_event(self.data_provider, self.rid, self.task_name)
        return {constants.key_success: True,
                constants.key_rid: self.rid}

    def prepare(self, message):
        self.params = message[constants.key_params]
        self.client_name = message[constants.key_client_name]

    def validate(self, message):
        assert isinstance(message.get(constants.key_client_name), str)
        params = message.get(constants.key_params)
        assert isinstance(params, dict)
        if any(p not in self.allowed_params for p in params):
            raise Exception(f'allowed params are {self.allowed_params}, got {list(params.keys())}')
