import pytest

from tests.test_operations.utils import *


MULTI_PARAMS_GOOD = [
    (4, 5, 20),
    (-12, 12, -144),
    (-25, -10, 250),
]

MULTI_INCORRECT_URLS = [
    "multiplications",
    "multi",
    "get_multiplication",
]


# Проверка правильности вычисляемого результата
@pytest.mark.parametrize("x, y, expected_result", MULTI_PARAMS_GOOD)
def test_multi_good(x: int, y: int, expected_result: int):
    results = preparation_for_test('multiplication', {"x": x, "y": y})
    assert results['statusCode'] == 0 and results['result'] == expected_result


# Проверка на возврат кода ошибки при неправильном указании параметров
@pytest.mark.parametrize("data", PARAMS_MISSING_ARGS)
def test_multi_not_enough_keys(data: dict):
    results = preparation_for_test('multiplication', data)
    assert results['statusCode'] == 2 and results['statusMessage'] == "Не указаны необходимые параметры"


# Проверка на возврат кода ошибки при неправильном указании типов данных параметров (! int)
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_TYPE)
def test_multi_incorrect_data(x, y):
    results = preparation_for_test('multiplication', {"x": x, "y": y})
    assert results['statusCode'] == 3 and results['statusMessage'] == "Значения параметров должны быть целыми"


# Проверка на возврат кода ошибки при превышении допустимых значений параметров
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_LIMITS)
def test_multi_limits(x, y):
    results = preparation_for_test('multiplication', {"x": x, "y": y})
    assert results['statusCode'] == 4 and results['statusMessage'] == "Превышены максимальные значения параметров"


# Проверка на возврат кода ошибки при неправильном формате тела запроса
@pytest.mark.parametrize("url", MULTI_INCORRECT_URLS)
def test_multi_incorrect_url(url: str):
    results = preparation_for_test(url, {"x": 1, "y": 2})
    assert results['statusCode'] == 5 and \
           results['statusMessage'] == f" {url} - Не верное имя задачи или тип HTTP запроса"


# Проверка на вызов исключения при отправке запроса на неактивный сервер
@pytest.mark.parametrize("host, port", DISABLE_SERVER_URLS)
def test_multi_try_operation_dis_server(host, port):
    with pytest.raises(ConnectionError):
        get_result_dis_server(host, port, 'multiplication', {"x": 1, "y": 2})
