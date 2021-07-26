from src.common import constants
from src.task_runners.base_controller import BaseController
from src.task_runners.surprise_service.surprise_task_handler import SurpriseTaskHandler


class SurpriseController(BaseController):
    def __init__(self, logger):
        super().__init__(logger, constants.task_name_surprise, constants.queue_url_surprise)

    def execute_message(self, message_to_handle: dict):
        handler = SurpriseTaskHandler(self.logger, self.data_provider)
        return handler.run(message_to_handle)
