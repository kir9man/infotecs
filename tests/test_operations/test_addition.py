import pytest
from typing import Dict, Tuple

from tests.test_operations.utils import *


ADD_PARAMS_GOOD = [
    (1, 2, 3),
    (1234, 321, 1555),
    (-10, -23, -33),
]

ADD_INCORRECT_URLS = [
    ("additions", ),
    ("show_sum", ),
    ("get_sum", ),
]


# Проверка правильности вычисляемого результата
@pytest.mark.parametrize("x, y, expected_result", ADD_PARAMS_GOOD, ids=get_ids(ADD_PARAMS_GOOD))
def test_addition_good(x: int, y: int, expected_result: int):
    result = preparation_for_test('addition', {"x": x, "y": y})
    assert result['statusCode'] == 0 and result['result'] == expected_result


# Проверка на возврат кода ошибки при неправильном указании параметров
@pytest.mark.parametrize("data", PARAMS_MISSING_ARGS, ids=get_ids(PARAMS_MISSING_ARGS))
def test_addition_not_enough_keys(data: Dict[str, int]):
    result = preparation_for_test('addition', data)
    assert result['statusCode'] == 2 and result['statusMessage'] == "Не указаны необходимые параметры"


# Проверка на возврат кода ошибки при неправильном указании типов данных параметров (! int)
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_TYPE, ids=get_ids(PARAMS_INCORRECT_TYPE))
def test_addition_incorrect_data(x, y):
    result = preparation_for_test('addition', {"x": x, "y": y})
    assert result['statusCode'] == 3 and result['statusMessage'] == "Значения параметров должны быть целыми"


# Проверка на возврат кода ошибки при превышении допустимых значений параметров
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_LIMITS, ids=get_ids(PARAMS_INCORRECT_LIMITS))
def test_addition_limits(x: int, y: int):
    result = preparation_for_test('addition', {"x": x, "y": y})
    assert result['statusCode'] == 4 and result['statusMessage'] == "Превышены максимальные значения параметров"


# Проверка на возврат кода ошибки при неправильном формате тела запроса
@pytest.mark.parametrize("url", ADD_INCORRECT_URLS, ids=get_ids(ADD_INCORRECT_URLS))
def test_addition_incorrect_url(url: Tuple[str]):
    result = preparation_for_test(url[0], {"x": 1, "y": 2})
    assert result['statusCode'] == 5 and \
           result['statusMessage'] == f" {url[0]} - Не верное имя задачи или тип HTTP запроса"


# Проверка на вызов исключения при отправке запроса на неактивный сервер
@pytest.mark.parametrize("host, port", DISABLE_SERVER_URLS, ids=get_ids(DISABLE_SERVER_URLS))
def test_add_try_operation_dis_server(host: str, port: str):
    with pytest.raises(ConnectionError):
        get_result_dis_server(host, port, 'addition', {"x": 1, "y": 2})
