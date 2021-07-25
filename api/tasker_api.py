import setproctitle
from flask import Flask, request

from api.handlers.sum2_api_handler import Sum2TaskApiHandler
from common import constants
from common.service_providers.data_provider import DataProvider
from common.databases_struct import jobs
from common.service_providers.queue_provider import QueueProvider
from common.tasker_logger import Logger

logger = Logger(constants.api_name)
data_provider = DataProvider(logger)
queue_provider = QueueProvider(logger)

app = Flask(__name__)

error_type_to_error_code = {
    constants.error_validation: 400,
    constants.error_process: 500
}

tasks_to_handlers = {
    constants.task_name_sum2: Sum2TaskApiHandler
}


@app.errorhandler(Exception)
def handle_error(error):
    return str(error), 500

@app.route('/tets')
def test():
    return {constants.key_success: True}, 200


@app.route('/get_requests_status')
def get_requests_status():
    request_data = request.get_json()
    client_name = request_data.get(constants.key_client_name)
    if client_name:
        job_status = data_provider.get_rows(jobs.table_name, [f'{jobs.key_client_name}={client_name}'])
        return {x[jobs.key_rid]: x[jobs.key_status] for x in job_status}
    return {constants.key_error: 'no client_name'}, 400


@app.route('/process', methods=['POST'])
def process():
    request_data = request.get_json()
    task = request_data.get(constants.key_task)
    if not task or task not in tasks_to_handlers:
        logger.error(f'request {request_data} is illegal')
        return {constants.key_error: f'{constants.key_task} is missing or contains an illegal task'}, 400
    request_data[constants.key_ip] = request.remote_addr
    handler = tasks_to_handlers[task](logger, data_provider, queue_provider)
    result = handler.run(request_data)
    if not result.get(constants.key_success):
        error_type = result.get(constants.key_error_type)
        error_code = error_type_to_error_code.get(error_type, 501)
        logger.error(
            f'got error {error_type} from handler {handler.task_name}, request: {request_data}, returning code {error_code}')
        return result, error_code
    return result


if __name__ == '__main__':
    setproctitle.setproctitle(f'tasker_{constants.api_name}')
    app.run(host='0.0.0.0', port=constants.api_port)
