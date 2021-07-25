import traceback

from common import constants


class BaseTaskHandler:
    def __init__(self, logger, data_provider, task_name):
        self.logger = logger
        self.data_provider = data_provider
        self.rid = None
        self.task_name = task_name
        self.params: dict = {}
        self.client_name: str = ''

    def run(self, message: dict) -> dict:
        self.logger.info(f'start handling message {message}')
        try:
            self.validate(message)
        except Exception as e:
            self.logger.error(f'validation failed for message {message}, cannot handle request')
            return {constants.key_success: False,
                    constants.key_error: f'validation failed due to {str(e)}',
                    constants.key_error_type: constants.error_validation}
        try:
            self.data_provider.create_connection()
            self.prepare()
            self.logger.info(f'start handling {self.task_name} request {self.rid} for client {self.client_name}')
            result = self.process(message)
            self.logger.info(f'done handling {self.task_name} request {self.rid} for client {self.client_name}')
            return result
        except Exception as e:
            self.logger.info(
                f'got exception {str(e)} while handling {self.task_name} request {self.rid} '
                f'for client {self.client_name}. trace: {traceback.format_exc()}')
            return {constants.key_success: False,
                    constants.key_error: f'process failed due to {str(e)}',
                    constants.key_error_type: constants.error_process}
        finally:
            self.data_provider.close_connection()

    def validate(self, message):
        pass

    def prepare(self):
        pass

    def process(self, message: dict) -> dict:
        raise Exception('not implemented')
