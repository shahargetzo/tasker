from src.common.service_providers.queue_provider import QueueProvider


class MockQueueProvider(QueueProvider):
    def __init__(self, logger):
        super().__init__(logger)
        self.messages = {}

    def send_to_queue(self, url: str, message: dict) -> bool:
        if url not in self.messages:
            self.messages[url] = []
        self.messages[url].append(message)
        return True

    def get_queue_messages(self, queue_url):
        url_messages = self.messages.get(queue_url)
        if url_messages:
            return url_messages[0]
