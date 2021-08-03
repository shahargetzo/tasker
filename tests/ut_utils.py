from src.common.tasker_logger import Logger
from tests.mocks.mock_data_provider import MockDataProvider
from tests.mocks.mock_queue_provider import MockQueueProvider

logger = Logger('test')
data_provider = MockDataProvider(logger)
queue_provider = MockQueueProvider(logger)


def get_logger():
    return logger


def get_data_provider():
    return data_provider


def get_queue_provider():
    return queue_provider
