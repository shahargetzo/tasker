from src.common import constants
from src.common.tasker_logger import Logger
from src.task_runners.surprise_service.surprise_controller import SurpriseController

if __name__ == '__main__':
    logger = Logger(constants.task_name_surprise)
    controller = SurpriseController(logger)
    logger.info(f'starting {controller.name}')
    controller.run()
