from common import constants
from task_runners.controllers.base_controller import BaseController
from task_runners.services.surprise_service.surprise_task_handler import SurpriseTaskHandler


class SurpriseController(BaseController):
    def __init__(self, logger):
        super().__init__(logger, constants.task_name_surprise, constants.queue_url_surprise)

    def execute_message(self, message_to_handle: dict):
        handler = SurpriseTaskHandler(self.logger, self.data_provider)
        return handler.run(message_to_handle)

