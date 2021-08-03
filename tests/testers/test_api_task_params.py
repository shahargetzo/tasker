from src.api.handlers import mult3_api_handler, sum2_api_handler, surprise_api_handler
from src.common import constants
from tests import ut_utils


def test_mult3_partial_params():
    func_name = test_mult3_partial_params.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    queue_provider = ut_utils.get_queue_provider()
    handler = mult3_api_handler.Mult3TaskApiHandler(logger, data_provider, queue_provider)
    res = handler.run({
        constants.key_client_name: 'test',
        constants.key_param_first: 1,
        constants.key_param_second: 1,
    })
    assert res, f'{func_name}: got empty response from handler'
    assert res.get(constants.key_error_type, '') == constants.error_validation, f'{func_name}: bad error type'
    assert not res.get(constants.key_success), f'{func_name}: success should be false'


def test_sum2_partial_params():
    func_name = test_sum2_partial_params.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    queue_provider = ut_utils.get_queue_provider()
    handler = sum2_api_handler.Sum2TaskApiHandler(logger, data_provider, queue_provider)
    res = handler.run({
        constants.key_client_name: 'test',
        constants.key_param_first: 1,
    })
    assert res, f'{func_name}: got empty response from handler'
    assert res.get(constants.key_error_type, '') == constants.error_validation, f'{func_name}: bad error type'
    assert not res.get(constants.key_success), f'{func_name}: success should be false'


def test_surprise_partial_params():
    func_name = test_surprise_partial_params.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    queue_provider = ut_utils.get_queue_provider()
    handler = surprise_api_handler.SurpriseTaskApiHandler(logger, data_provider, queue_provider)
    res = handler.run({
        constants.key_client_name: 'test',
        constants.key_param_second: 1,
    })
    assert res, f'{func_name}: got empty response from handler'
    assert res.get(constants.key_error_type, '') == constants.error_validation, f'{func_name}: bad error type'
    assert not res.get(constants.key_success), f'{func_name}: success should be false'


def test_mult3_type_params():
    func_name = test_mult3_type_params.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    queue_provider = ut_utils.get_queue_provider()
    handler = mult3_api_handler.Mult3TaskApiHandler(logger, data_provider, queue_provider)
    res = handler.run({
        constants.key_client_name: 'test',
        constants.key_param_first: '1',
        constants.key_param_second: 1,
        constants.key_param_third: [1],
    })
    assert res, f'{func_name}: got empty response from handler'
    assert res.get(constants.key_error_type, '') == constants.error_validation, f'{func_name}: bad error type'
    assert not res.get(constants.key_success), f'{func_name}: success should be false'


def test_sum2_type_params():
    func_name = test_sum2_type_params.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    queue_provider = ut_utils.get_queue_provider()
    handler = sum2_api_handler.Sum2TaskApiHandler(logger, data_provider, queue_provider)
    res = handler.run({
        constants.key_client_name: 'test',
        constants.key_param_first: 1,
        constants.key_param_second: {"a": 1},
    })
    assert res, f'{func_name}: got empty response from handler'
    assert res.get(constants.key_error_type, '') == constants.error_validation, f'{func_name}: bad error type'
    assert not res.get(constants.key_success), f'{func_name}: success should be false'


def test_surprise_type_params():
    func_name = test_surprise_type_params.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    queue_provider = ut_utils.get_queue_provider()
    handler = surprise_api_handler.SurpriseTaskApiHandler(logger, data_provider, queue_provider)
    res = handler.run({
        constants.key_client_name: 'test',
        constants.key_param_first: 'a',
    })
    assert res, f'{func_name}: got empty response from handler'
    assert res.get(constants.key_error_type, '') == constants.error_validation, f'{func_name}: bad error type'
    assert not res.get(constants.key_success), f'{func_name}: success should be false'
