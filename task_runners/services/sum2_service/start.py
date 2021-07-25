from common.tasker_logger import Logger
from task_runners.services.sum2_service.sum2_controller import Sum2Controller

if __name__ == '__main__':
    logger = Logger('start')
    controller = Sum2Controller()
    logger.info(f'starting {controller.name}')
    controller.run()
