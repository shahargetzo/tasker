from common import constants
from task_runners.controllers.base_controller import BaseController
from task_runners.services.sum2_service.sum2_task_handler import Sum2TaskHandler


class Sum2Controller(BaseController):
    def __init__(self, logger):
        super().__init__(logger, constants.task_name_sum2, constants.queue_url_sum2)

    def execute_message(self, message_to_handle: dict):
        handler = Sum2TaskHandler(self.logger, self.data_provider)
        return handler.run(message_to_handle)

