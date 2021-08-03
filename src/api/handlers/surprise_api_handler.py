from src.api.handlers.base_api_handler import BaseAPIHandler
from src.common import constants


class SurpriseTaskApiHandler(BaseAPIHandler):
    def __init__(self, logger, data_provider, queue_provider):
        super().__init__(logger, data_provider, queue_provider, constants.task_name_surprise,
                         constants.queue_url_surprise, [constants.key_param_first, ])

    def validate(self, message):
        super().validate(message)
        params = message[constants.key_params]
        assert isinstance(params.get(constants.key_param_first), int)
