import pytest
from typing import Dict, Tuple

from tests.test_operations.utils import *


MULTI_PARAMS_GOOD = [
    (4, 5, 20),
    (-12, 12, -144),
    (-25, -10, 250),
]

MULTI_INCORRECT_URLS = [
    ("multiplications", ),
    ("multi", ),
    ("get_multiplication", ),
]


# Проверка правильности вычисляемого результата
@pytest.mark.parametrize("x, y, expected_result", MULTI_PARAMS_GOOD, ids=get_ids(MULTI_PARAMS_GOOD))
def test_multi_good(x: int, y: int, expected_result: int):
    results = preparation_for_test('multiplication', {"x": x, "y": y})
    assert results['statusCode'] == 0 and results['result'] == expected_result


# Проверка на возврат кода ошибки при неправильном указании параметров
@pytest.mark.parametrize("data", PARAMS_MISSING_ARGS, ids=get_ids(PARAMS_MISSING_ARGS))
def test_multi_not_enough_keys(data: Dict[str, int]):
    results = preparation_for_test('multiplication', data)
    assert results['statusCode'] == 2 and results['statusMessage'] == "Не указаны необходимые параметры"


# Проверка на возврат кода ошибки при неправильном указании типов данных параметров (! int)
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_TYPE, ids=get_ids(PARAMS_INCORRECT_TYPE))
def test_multi_incorrect_data(x, y):
    results = preparation_for_test('multiplication', {"x": x, "y": y})
    assert results['statusCode'] == 3 and results['statusMessage'] == "Значения параметров должны быть целыми"


# Проверка на возврат кода ошибки при превышении допустимых значений параметров
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_LIMITS, ids=get_ids(PARAMS_INCORRECT_LIMITS))
def test_multi_limits(x: int, y: int):
    results = preparation_for_test('multiplication', {"x": x, "y": y})
    assert results['statusCode'] == 4 and results['statusMessage'] == "Превышены максимальные значения параметров"


# Проверка на возврат кода ошибки при неправильном формате тела запроса
@pytest.mark.parametrize("url", MULTI_INCORRECT_URLS, ids=get_ids(MULTI_INCORRECT_URLS))
def test_multi_incorrect_url(url: Tuple[str]):
    results = preparation_for_test(url[0], {"x": 1, "y": 2})
    assert results['statusCode'] == 5 and \
           results['statusMessage'] == f" {url[0]} - Не верное имя задачи или тип HTTP запроса"


# Проверка на вызов исключения при отправке запроса на неактивный сервер
@pytest.mark.parametrize("host, port", DISABLE_SERVER_URLS, ids=get_ids(DISABLE_SERVER_URLS))
def test_multi_try_operation_dis_server(host: str, port: str):
    with pytest.raises(ConnectionError):
        get_result_dis_server(host, port, 'multiplication', {"x": 1, "y": 2})
