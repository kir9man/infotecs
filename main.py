import os
from datetime import datetime

# Директории/модули тестирования
TYPE_TEST = {
    'all': {'path': 'tests', 'name': 'all_tests'},
    'all_com': {'path': 'tests/test_commands', 'name': 'all_commands'},
    'all_op': {'path': 'tests/test_operations', 'name': 'all_operations'},
    'only_com': {'path': 'tests/test_commands/test_commands.py', 'name': 'only_commands'},
    'only_st': {'path': 'tests/test_commands/test_state.py', 'name': 'only_state'},
    'only_add': {'path': 'tests/test_operations/test_addition.py', 'name': 'only_addition'},
    'only_div': {'path': 'tests/test_operations/test_division.py', 'name': 'only_division'},
    'only_mul': {'path': 'tests/test_operations/test_multiplication.py', 'name': 'only_multiplication'},
    'only_rem': {'path': 'tests/test_operations/test_remainder.py', 'name': 'only_remainder'},
}


# Создает директорию, если ее не существует в каталоге './logs'
def create_directory() -> str:
    now_date = datetime.now().strftime("%d-%m-%Y")
    if now_date not in os.listdir('logs'):
        os.makedirs(f'logs/{now_date}')
    return now_date


# Формирует имя файла формата test[номер теста на текущий день]_[тип теста]([время теста: часы-минуты])
def create_log_file_name(path: str, type_test: str) -> str:
    now_time = datetime.now().strftime("%H-%M")
    return f"test{len(os.listdir('logs/' + path)) + 1}_{type_test}({now_time})"


# Добавление к имени файла результата теста 'FAILED' или 'PASSED'
def result_test(directory: str, file_name: str) -> str:
    with open(f"logs/{directory}/{file_name}.txt", 'r', encoding='UTF8') as log_file:
        return 'FAILED' if any(['FAILED' in string for string in log_file.readlines()]) else 'PASSED'


def main():
    global TYPE_TEST
    type_test = TYPE_TEST['all_op']
    directory = create_directory()
    file_name = create_log_file_name(directory, type_test['name'])
    os.system(f"pytest -v {type_test['path']} >logs/{directory}/{file_name}.txt")
    os.rename(f"logs/{directory}/{file_name}.txt",
              f"logs/{directory}/{file_name}-{result_test(directory, file_name)}.txt")


if __name__ == '__main__':
    main()
