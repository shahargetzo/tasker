import random

from src.common import constants
from src.common.databases_struct import job_events
from src.common.databases_struct import jobs
from src.task_runners.base_task_queue_handler import BaseTaskQueueHandler

sentences = [
    'trilili_tralala',
    'mi_sheshota_rak_maim',
    'yesh_la_harbe_sodot',
    'yom_shelo_nehshav_lo_sofrim',
    'tarimu_la_tarimu',
    'al_tarutzi_ksheyorim_alaich',
    'ki_tamuti_ayefa',
    'ani_lo_nehenet',
]


class SurpriseTaskHandler(BaseTaskQueueHandler):
    def __init__(self, logger, data_provider):
        super().__init__(logger, data_provider, constants.task_name_surprise)

    def process(self, message: dict) -> dict:
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_start_process)
        sentence = random.choice(sentences)
        result = f'{sentence}_{self.params[constants.key_param_first]}'
        jobs.update_job(self.data_provider, self.rid, jobs.status_done, result)
        job_events.insert_event(self.data_provider, self.rid, job_events.event_name_end_process)
        return {constants.key_success: True}
