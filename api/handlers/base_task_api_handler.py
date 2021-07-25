import uuid

from common.base_handler import BaseTaskHandler


class BaseTaskAPIHandler(BaseTaskHandler):
    def __init__(self, logger, data_provider, queue_provider, task_name):
        super().__init__(logger, data_provider, task_name)
        self.queue_provider = queue_provider
        self.rid = uuid.uuid4().hex
