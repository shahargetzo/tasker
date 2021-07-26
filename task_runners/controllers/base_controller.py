import json
import traceback
from time import sleep

import setproctitle

from common.service_providers.data_provider import DataProvider
from common.databases_struct import process_config
from common.service_providers.queue_provider import QueueProvider, QueueException


class BaseController:
    def __init__(self, logger, name, queue_url):
        self.logger = logger
        self.name = name
        self.queue_url = queue_url
        self.data_provider = DataProvider(self.logger)
        self.queue_provider = QueueProvider(self.logger)
        self.process_title = f'tasker_{name}'
        setproctitle.setproctitle(self.process_title)

    def run(self):
        try:
            self.data_provider.create_connection()
            self.prepare()
            self.start_listening()
        except Exception as e:
            self.logger.error(
                f'got exception while running. name: {self.name}, error: {str(e)}, trace: {traceback.format_exc()}')
            try:
                process_config.update_process_status(self.data_provider, self.name, process_config.status_error)
            except Exception as e:
                self.logger.error(f'failed to update process {self.name} status to {process_config.status_error}: {e}')
            self.kill_self()
        finally:
            self.data_provider.close_connection()

    def prepare(self):
        pass

    def kill_self(self):
        self.data_provider.close_connection()
        self.logger.warning(f'killing controller {self.name}')
        exit(1)

    def start_listening(self):
        while True:
            process_status = process_config.get_process_status(self.data_provider, self.name)
            if not process_status or process_status[0].get(process_config.key_status, '') != process_config.status_active:
                self.logger.warning(
                    f'process {self.name} has no row in {process_config.table_name} or status is not active, killing self')
                self.kill_self()
            try:
                message = self.queue_provider.get_queue_messages(self.queue_url)
                if not message:
                    # self.logger.debug(f'no messages to handle for {self.name}, queue {self.queue_url}')
                    sleep(2)
                    continue
                message_to_handle = json.loads(message['Body'])
                if 'kill' in message_to_handle:
                    self.logger.warning(f'got message {message_to_handle} with kill request, killing self')
                    self.kill_self()
                self.execute_message(message_to_handle)
            except QueueException as e:
                self.logger.error(f'failed to get messages from queue {self.queue_url}: {str(e)}. closing controller')
                process_config.update_process_status(self.data_provider, self.name, process_config.status_queue)
                self.kill_self()

    def execute_message(self, message_to_handle: dict):
        pass
