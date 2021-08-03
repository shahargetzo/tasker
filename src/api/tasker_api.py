import traceback

import setproctitle
from flask import Flask, request, jsonify

from src.api.handlers.mult3_api_handler import Mult3TaskApiHandler
from src.api.handlers.sum2_api_handler import Sum2TaskApiHandler
from src.api.handlers.surprise_api_handler import SurpriseTaskApiHandler
from src.common import constants
from src.common.databases_struct import process_config, jobs
from src.common.service_providers.data_provider import DataProvider, DBWhere
from src.common.service_providers.queue_provider import QueueProvider
from src.common.tasker_logger import Logger

logger = Logger(constants.api_name)
data_provider = DataProvider(logger)
queue_provider = QueueProvider(logger)

app = Flask(__name__)

error_type_to_error_code = {
    constants.error_validation: 400,
    constants.error_process: 500
}

tasks_to_handlers = {
    constants.task_name_sum2: Sum2TaskApiHandler,
    constants.task_name_mult3: Mult3TaskApiHandler,
    constants.task_name_surprise: SurpriseTaskApiHandler,
}


@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'got exception: {traceback.format_exc()}')
    return str(error), 500


@app.route('/test')
def test():
    return {constants.key_success: True}, 200


@app.route('/get_requests_status')
def get_requests_status():
    request_data = request.get_json()
    client_name = request_data.get(constants.key_client_name)
    if client_name:
        job_status = data_provider.get_rows(jobs.table_name, [DBWhere(jobs.key_client_name, '=', client_name)])
        return {x[jobs.key_rid]: x for x in job_status}
    return {constants.key_error: 'no client_name'}, 400


@app.route('/get_processes_status')
def get_processes_status():
    processes_status = data_provider.get_rows(process_config.table_name)
    return {x[process_config.key_process_name]: x[process_config.key_status] for x in processes_status}


@app.route('/set_processes_status')
def set_processes_status():
    request_data = request.get_json()
    updated = {}
    for p in request_data:
        if p not in constants.available_processes:
            updated.update({p: {constants.key_error: f'got unknown process: {p}'}})
            continue
        p_status = request_data[p]
        if p_status not in process_config.available_statuses:
            updated.update({p: {constants.key_error: f'got unknown status got process {p}: {p_status}'}})
            continue
        process_config.update_process_status(data_provider, p, p_status)
        updated[p] = f'updated to  {p_status}'
    return updated


@app.route('/process', methods=['POST'])
def process():
    request_data = request.get_json()
    task = request_data.get(constants.key_task)
    if not task or task not in tasks_to_handlers:
        logger.error(f'request task {task} is illegal')
        return jsonify({constants.key_error: f'{constants.key_task} is missing or contains an illegal task'}), 400
    request_data[constants.key_ip] = request.remote_addr
    handler = tasks_to_handlers[task](logger, data_provider, queue_provider)
    result = handler.run(request_data)
    if not result.get(constants.key_success):
        error_type = result.get(constants.key_error_type)
        error_code = error_type_to_error_code.get(error_type, 501)
        logger.error(
            f'got error {error_type}:{result.get(constants.key_error)} from handler {handler.task_name}, '
            f'request: {request_data}, returning code {error_code}')
        return jsonify(result), error_code
    return result


if __name__ == '__main__':
    setproctitle.setproctitle(f'tasker_{constants.api_name}')
    app.run(host='0.0.0.0', port=constants.api_port)
