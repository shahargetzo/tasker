from api.handlers.base_task_api_handler import BaseTaskAPIHandler
from common import constants


class Mult3TaskApiHandler(BaseTaskAPIHandler):
    def __init__(self, logger, data_provider, queue_provider):
        super().__init__(logger, data_provider, queue_provider, constants.task_name_mult3, constants.queue_url_mult3)

    def validate(self, message):
        super().validate(message)
        params = message[constants.key_params]
        assert isinstance(params.get('first'), int)
        assert isinstance(params.get('second'), int)
        assert isinstance(params.get('third'), int)
