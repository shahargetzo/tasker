from src.common import constants
from src.common.tasker_logger import Logger
from src.task_runners.sum2_service.sum2_controller import Sum2Controller

if __name__ == '__main__':
    logger = Logger(constants.task_name_sum2)
    controller = Sum2Controller(logger)
    logger.info(f'starting {controller.name}')
    controller.run()
