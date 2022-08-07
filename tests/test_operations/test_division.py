import pytest

from tests.test_operations.utils import *


DIV_PARAMS_GOOD = [
    (11, 3, 3),
    (54, 6, 9),
    (1000, -10, -100),
]

DIV_INCORRECT_URLS = [
    "divisions",
    "div",
    "show_div",
]


# Проверка правильности вычисляемого результата
@pytest.mark.parametrize("x, y, expected_result", DIV_PARAMS_GOOD)
def test_division_good(x: int, y: int, expected_result: int):
    results = preparation_for_test('division', {"x": x, "y": y})
    assert results['statusCode'] == 0 and results['result'] == expected_result


# Проверка на возврат кода ошибки при неправильном указании параметров
@pytest.mark.parametrize("data", PARAMS_MISSING_ARGS)
def test_division_not_enough_keys(data: dict):
    results = preparation_for_test('division', data)
    assert results['statusCode'] == 2 and results['statusMessage'] == "Не указаны необходимые параметры"


# Проверка на возврат кода ошибки при неправильном указании типов данных параметров (! int)
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_TYPE)
def test_division_incorrect_data(x, y):
    results = preparation_for_test('division', {"x": x, "y": y})
    assert results['statusCode'] == 3 and results['statusMessage'] == "Значения параметров должны быть целыми"


# Проверка на возврат кода ошибки при превышении допустимых значений параметров
@pytest.mark.parametrize("x, y", PARAMS_INCORRECT_LIMITS)
def test_division_limits(x, y):
    results = preparation_for_test('division', {"x": x, "y": y})
    assert results['statusCode'] == 4 and results['statusMessage'] == "Превышены максимальные значения параметров"


# Проверка на возврат кода ошибки при неправильном формате тела запроса
@pytest.mark.parametrize("url", DIV_INCORRECT_URLS)
def test_division_incorrect_url(url: str):
    results = preparation_for_test( url, {"x": 1, "y": 2})
    assert results['statusCode'] == 5 and \
           results['statusMessage'] == f" {url} - Не верное имя задачи или тип HTTP запроса"


# Проверка на возврат кода ошибки при делении на ноль
@pytest.mark.parametrize("x, y", PARAMS_ZERO_DIVISION)
def test_division_zero_div(x, y):
    results = preparation_for_test('division', {"x": x, "y": y})
    assert results['statusCode'] == 8 and results['statusMessage'] == "Ошибка вычисления"


# Проверка на вызов исключения при отправке запроса на неактивный сервер
@pytest.mark.parametrize("host, port", DISABLE_SERVER_URLS)
def test_div_try_operation_dis_server(host, port):
    with pytest.raises(ConnectionError):
        get_result_dis_server(host, port, 'division', {"x": 1, "y": 2})

