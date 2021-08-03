from src.common import constants
from src.task_runners.mult3_service import mult3_task_handler
from src.task_runners.sum2_service import sum2_task_handler
from src.task_runners.surprise_service import surprise_task_handler
from tests import ut_utils


def test_surprise_task_handler():
    func_name = test_surprise_task_handler.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    handler = surprise_task_handler.SurpriseTaskHandler(logger, data_provider)
    res = handler.get_result({constants.key_param_first: 1})
    assert res, f'{func_name}: got empty res'
    assert res.split('_')[-1] == 1, f'{func_name}: res for {handler.task_name} does not end with first param'


def test_sum2_task_handler():
    func_name = test_sum2_task_handler.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    handler = sum2_task_handler.Sum2TaskHandler(logger, data_provider)
    res = handler.get_result({constants.key_param_first: 1, constants.key_param_second: 2})
    assert res, f'{func_name}: got empty res'
    assert res == 3, f'{func_name}: res for {handler.task_name} does not match expected result'


def test_mult3_task_handler():
    func_name = test_mult3_task_handler.__name__
    logger = ut_utils.get_logger()
    data_provider = ut_utils.get_data_provider()
    handler = mult3_task_handler.Mult3TaskHandler(logger, data_provider)
    res = handler.get_result(
        {constants.key_param_first: 1, constants.key_param_second: 2, constants.key_param_third: 3})
    assert res, f'{func_name}: got empty res'
    assert res == 6, f'{func_name}: res for {handler.task_name} does not match expected result'
