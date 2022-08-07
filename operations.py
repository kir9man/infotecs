import json
import requests

from commands import check_connect


# вычисление результата
def get_math_operation(host: str, port: str, operation: str,  data: dict) -> dict:
    if not check_connect(host, port)['statusCode']:
        rqst = requests.post(f"http://{host}:{port}/api/{operation}", data=json.dumps(data))
        return rqst.json()
    raise ConnectionError(f"Сервер недоступен")


# функция state
def show_state(host: str, port: str):
    return check_connect(host, port)


