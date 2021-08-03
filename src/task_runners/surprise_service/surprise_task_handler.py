import random

from src.common import constants
from src.task_runners.base_queue_handler import BaseQueueHandler

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


class SurpriseTaskHandler(BaseQueueHandler):
    def __init__(self, logger, data_provider):
        super().__init__(logger, data_provider, constants.task_name_surprise)

    def get_result(self, params: dict) -> str:
        sentence = random.choice(sentences)
        return f'{sentence}_{self.params[constants.key_param_first]}'
