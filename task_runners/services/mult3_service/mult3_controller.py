from common import constants
from task_runners.controllers.base_controller import BaseController
from task_runners.services.mult3_service.mult3_task_handler import Mult3TaskHandler


class Mult3Controller(BaseController):
    def __init__(self, logger):
        super().__init__(logger, constants.task_name_mult3, constants.queue_url_mult3)

    def execute_message(self, message_to_handle: dict):
        handler = Mult3TaskHandler(self.logger, self.data_provider)
        return handler.run(message_to_handle)

