import json

import boto3

from src.common import constants


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
        self.logger.debug(f'sending message {message} to queue {url}')
        try:
            self.client.send_message(
                QueueUrl=url,
                MessageBody=json.dumps(message),
            )
            return True
        except Exception as e:
            self.logger.error(f'failed sending message to queue: {str(e)}')
            return False

    def get_queue_messages(self, queue_url):
        try:
            response = self.client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1
            )
            if response:
                messages = response.get('Messages')
                if messages:
                    self.logger.debug('successfully got a message, deleting from sqs')
                    message = messages[0]
                    self.client.delete_message(QueueUrl=queue_url,
                                               ReceiptHandle=message['ReceiptHandle'])
                    return message
        except Exception as e:
            raise QueueException(str(e))
