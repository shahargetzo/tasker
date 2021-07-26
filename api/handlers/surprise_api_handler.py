from api.handlers.base_task_api_handler import BaseTaskAPIHandler
from common import constants


class SurpriseTaskApiHandler(BaseTaskAPIHandler):
    def __init__(self, logger, data_provider, queue_provider):
        super().__init__(logger, data_provider, queue_provider, constants.task_name_surprise, constants.queue_url_surprise)

    def validate(self, message):
        super().validate(message)
        params = message[constants.key_params]
        assert isinstance(params.get('first'), int)
