import json

import boto3

from common import constants


class QueueException(Exception):
    def __init__(self, message):
        super().__init__(message)


class QueueProvider:
    def __init__(self, logger):
        self.logger = logger
        self.client = boto3.client('sqs',
                                   region_name='us-west-2',
                                   aws_secret_access_key=constants.aws_secret_access_key,
                                   aws_access_key_id=constants.aws_access_key_id)

    def send_to_queue(self, url: str, message: dict):
        try:
            self.client.send_message(
                QueueUrl=url,
                MessageBody=json.dumps(message),
            )
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def get_queue_messages(self, queue_url):
        try:
            response = self.client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1
            )
            self.logger.debug(f'got response from queue {queue_url}: {response}')
            if response:
                messages = response.get('Messages')
                if messages:
                    message = messages[0]
                    self.client.delete_message(QueueUrl=queue_url,
                                               ReceiptHandle=message['ReceiptHandle'])
                    return message
        except Exception as e:
            raise QueueException(str(e))
