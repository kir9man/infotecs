import pytest

from tests.test_operations.utils import *


ADDITION_PARAMS_GOOD = [
    (1, 2, 3),
    (1234, 321, 1555),
    (-10, -23, -33),
]

ADDITION_INCORRECT_URLS = [
    "additions",
    "show_sum",
    "get_sum",
]


# Проверка правильности вычисляемого результата
@pytest.mark.parametrize("x, y, expected_result", ADDITION_PARAMS_GOOD)
def test_addition_good(x: int, y: int, expected_result: int):
    result = preparation_for_test('addition', {"x": x, "y": y})
    assert result['statusCode'] == 0 and result['result'] == expected_result


# Проверка на возврат кода ошибки при неправильном указании параметров
@pytest.mark.parametrize("data", PARAMS_MISSING_ARGS)
def test_addition_not_enough_keys(data: dict):
    result = preparation_for_test('addition', data)
    assert result['statusCode'] == 2 and result['statusMessage'] == "Не указаны необходимые параметры"


# Проверка на возврат кода ошибки при неправильном указании типов данных параметров (! int)
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_TYPE)
def test_addition_incorrect_data(x, y):
    result = preparation_for_test('addition', {"x": x, "y": y})
    assert result['statusCode'] == 3 and result['statusMessage'] == "Значения параметров должны быть целыми"


# Проверка на возврат кода ошибки при превышении допустимых значений параметров
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_LIMITS)
def test_addition_limits(x, y):
    result = preparation_for_test('addition', {"x": x, "y": y})
    assert result['statusCode'] == 4 and result['statusMessage'] == "Превышены максимальные значения параметров"


# Проверка на возврат кода ошибки при неправильном формате тела запроса
@pytest.mark.parametrize("url", ADDITION_INCORRECT_URLS)
def test_addition_incorrect_url(url: str):
    result = preparation_for_test(url, {"x": 1, "y": 2})
    assert result['statusCode'] == 5 and \
           result['statusMessage'] == f" {url} - Не верное имя задачи или тип HTTP запроса"


# Проверка на вызов исключения при отправке запроса на неактивный сервер
@pytest.mark.parametrize("host, port", DISABLE_SERVER_URLS)
def test_add_try_operation_dis_server(host, port):
    with pytest.raises(ConnectionError):
        get_result_dis_server(host, port, 'addition', {"x": 1, "y": 2})
