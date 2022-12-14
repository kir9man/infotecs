import pytest

from commands import stop_api


@pytest.fixture(scope='session', autouse=True)
def stop_api_before_test():
    stop_api()
    yield
    stop_api()
