from src.api.handlers.base_task_api_handler import BaseTaskAPIHandler
from src.common import constants


class Mult3TaskApiHandler(BaseTaskAPIHandler):
    def __init__(self, logger, data_provider, queue_provider):
        super().__init__(logger, data_provider, queue_provider, constants.task_name_mult3, constants.queue_url_mult3,
                         [constants.key_param_first,
                          constants.key_param_second,
                          constants.key_param_third, ])

    def validate(self, message):
        super().validate(message)
        params = message[constants.key_params]
        assert isinstance(params.get(constants.key_param_first), int)
        assert isinstance(params.get(constants.key_param_second), int)
        assert isinstance(params.get(constants.key_param_third), int)
