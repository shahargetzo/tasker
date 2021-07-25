from time import sleep

import psutil as psutil

import start_tasker
from common import constants
from common.databases_struct import process_config
from task_runners.controllers.base_controller import BaseController

processes_to_run = {
    f'tasker_{constants.api_name}': {'run': start_tasker.start_api()},
    f'tasker_{constants.task_name_sum2}': {'run': start_tasker.start_sum2_controller()}
}


class ProcessController(BaseController):
    def __init__(self):
        super().__init__(constants.task_name_process_controller, None)

    def start_listening(self):
        running_processes = {}
        for proc in psutil.process_iter():
            try:
                process_name = proc.name()
                if process_name in processes_to_run:
                    running_processes[process_name] = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        for ptr in processes_to_run:
            if ptr not in running_processes:
                process_status = process_config.get_process_status(self.data_provider, ptr)
                if not process_status or process_status[0].get(process_config.key_status,
                                                            '') != process_config.status_active:
                    self.logger.warning(
                        f'process {ptr} has no row in {process_config.table_name} or status os not actvie, not starting')
                    continue
                self.logger.info(f'process {ptr} is not running. start now...')
                try:
                    processes_to_run[ptr]['run']()
                except Exception as e:
                    self.logger.error(f'failed to start process {ptr}: {str(e)}')
        sleep(10)
