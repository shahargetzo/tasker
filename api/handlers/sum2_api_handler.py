from api.handlers.base_task_api_handler import BaseTaskAPIHandler
from common import constants
from common.databases_struct import jobs, job_events


class Sum2TaskApiHandler(BaseTaskAPIHandler):
    def __init__(self, logger, data_provider, queue_provider):
        super().__init__(logger, data_provider, queue_provider, constants.task_name_sum2)

    def validate(self, message):
        assert isinstance(message.get(constants.key_client_name), str)
        assert isinstance(message.get(constants.key_params), dict)
        self.params = message[constants.key_params]
        assert isinstance(self.params.get('first'), int)
        assert isinstance(self.params.get('second'), int)

    def process(self, message: dict) -> dict:
        self.client_name = message[constants.key_client_name]
        sql_success = jobs.insert_job(self.data_provider, self.rid, self.client_name, constants.task_name_sum2,
                                      self.params, message.get(constants.key_ip))
        if not sql_success:
            self.logger.error('failed to enter request to db')
            return {constants.key_success: False,
                    constants.key_error: 'internal'}

        queue_success = self.queue_provider.send_to_queue(constants.sum2_queue_url, {'rid': self.rid})
        if not queue_success:
            self.logger.error('failed to send request to queue')
            return {constants.key_success: False,
                    constants.key_error: 'internal'}
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_insert_to_queue)
        return {constants.key_success: True,
                constants.key_rid: self.rid}
