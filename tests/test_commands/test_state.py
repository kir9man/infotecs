import pytest

from commands import run_api, check_connect, stop_api
from utils import URLS


# Проверка правильности кода возврата get запроса /state активного сервера
@pytest.mark.parametrize('url', URLS)
def test_state_activate_server(url):
    run_api(*url)
    result = check_connect(*url)
    assert result['statusCode'] == 0 and result['state'] == 'OК'


# Проверка правильности кода возврата get запроса /state неактивного сервера
@pytest.mark.parametrize('url', URLS)
def test_state_disable_server(url):
    stop_api()
    result = check_connect(*url)
    host = '127.0.0.1' if not url else url[0]
    port = '17678' if len(url) != 2 else url[1]
    assert result['statusCode'] == 1 and result['statusMessage'] == f"Сервер {host}:{port} недоступен"


