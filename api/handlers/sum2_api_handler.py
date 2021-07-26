from api.handlers.base_task_api_handler import BaseTaskAPIHandler
from common import constants


class Sum2TaskApiHandler(BaseTaskAPIHandler):
    def __init__(self, logger, data_provider, queue_provider):
        super().__init__(logger, data_provider, queue_provider, constants.task_name_sum2, constants.queue_url_sum2)

    def validate(self, message):
        super().validate(message)
        params = message[constants.key_params]
        assert isinstance(params.get('first'), int)
        assert isinstance(params.get('second'), int)
