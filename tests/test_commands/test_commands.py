import pytest

from commands import *
from tests.test_commands.utils import URLS, URLS_IDS


# Проверка правильности запуска приложения webcalculator.exe
@pytest.mark.parametrize("url", URLS, ids=URLS_IDS)
def test_start_api(url):
    run_api(*url)
    result = check_connect(*url)['statusCode']
    assert result == 0


# Проверка правильности остановки приложения webcalculator.exe
@pytest.mark.parametrize("url", URLS, ids=URLS_IDS)
def test_stop_api(url):
    run_api(*url)
    calc_was_started = not bool(check_connect(*url)['statusCode'])
    stop_api()
    assert check_connect()['statusCode'] == 1 and calc_was_started


# Проверка правильности перезапуска приложения webcalculator.exe
@pytest.mark.parametrize("url", URLS, ids=URLS_IDS)
def test_restart_api(url):
    run_api(*url)
    ping_started_api = not bool(check_connect(*url)['statusCode'])
    restart_api(*url)
    ping_started_api_again = not bool(check_connect(*url)['statusCode'])
    assert ping_started_api and ping_started_api_again

