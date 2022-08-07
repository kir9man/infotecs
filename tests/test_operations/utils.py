from operations import get_math_operation
from commands import run_api, stop_api


HOST = '127.0.0.1'
PORT = '17678'

PARAMS_MISSING_ARGS = [
    ({"k": 1, "z": 2}),
    ({"x": 3, "z": 4}),
    ({"z": 5, "y": 6}),
    ({"x": 7}),
    ({"y": 8}),
]

PARAMS_INCORRECT_TYPE = [
    (1, 1.1),
    ("1", 1.1),
    (1, [1]),
]

PARAMS_INCORRECT_LIMITS = [
    (-2147483649, 2147483648),
    (-2147483649, 500),
    (23, 2147483648),
]

PARAMS_ZERO_DIVISION = [
    (1, 0),
    (5123, 0),
    (-11, 0),
]

DISABLE_SERVER_URLS = [
    ('127.0.0.1', '17678'),
    ('127.31.255.255', '8080'),
    ('localhost', '5413'),
]


def preparation_for_test(operation: str, data: dict):
    global HOST, PORT
    run_api(HOST, PORT)
    return get_math_operation(HOST, PORT, operation, data)


def get_result_dis_server(host: str, port: str, operation: str, data: dict):
    stop_api()
    return get_math_operation(host, port, operation, data)
