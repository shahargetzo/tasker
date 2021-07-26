from common import constants
from common.tasker_logger import Logger
from task_runners.services.mult3_service.mult3_controller import Mult3Controller

if __name__ == '__main__':
    logger = Logger(constants.task_name_mult3)
    controller = Mult3Controller(logger)
    logger.info(f'starting {controller.name}')
    controller.run()
