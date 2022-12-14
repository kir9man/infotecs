# Автотесты для webcalculator
_____

Тестовое задание для "Infotecs".<br/>
Исполнитель - Иванов Кирилл.<br/>
Инструменты - python 3.10, pytest, os, requests.

Все зависимости проекта указаны в <b>requirements.txt</b>.  


## 1. Запуск

Для запуска автотестов необходимо запустить скрипт <b>main.py</b> или настроить конфигурацию pytest в IDE.

При запуске модуля <b>main.py</b> также имеется возможность выбора директории\модуля тестирования. Для этого 
необходимо в функции <b>main()</b> указать ключ требуемого типа теста.

`type_test = TYPE_TEST[<Тип теста>]`

Возможные варианты: 

- 'all' - запуск всех тестов;
- 'all_com' - тестирование команд управления приложения(start, stop, state, restart);
- 'all_op' - тестирование основного функционала(сложение, вычитание и т.д.);
- 'only_com' - тестирование команд управления приложения (без state);
- 'only_st' - тестирование state;
- 'only_add' - только операция сложения;
- 'only_div': только операция деления;
- 'only_mul': только операция умножения;
- 'only_ren': только операция вычисления остатка от деления;


## 2. Структура проекта 

Для взаимодействия с тестируемым приложением в корневой директории проекта реализованы модули 
<b>commands.py</b> и <b>operations.py</b>. В них инициированы функции, которые обеспечивают управление
приложением согласно описанию, представленного в документе "Приложение к ТЗ".

- commands.py - команды управления приложением(start, stop и т.д);
- operations.py - математические операции;

Реализованные автотесты размещены в папке <b>"tests"</b>. Модули тестирования команд управления расположены в 
<b>"tests/test_commands"</b>, модули тестирования вычислительных операций - <b>"tests/test_operations"</b>

Проект содержит 101 тестовый кейс с учетом параметризации тестовых функций.


## 3. test_commands

Директория содержит:

- conftest.py - для размещения фикстуры <b>stop_api_before_test</b>;
- test_commands.py - тестовый модуль команд управления;
- test_state.py - тестовый модуль команды state;
- utils.py - для размещения дополнительной логики используемой в тестах директории test_commands.

### 3.1 test_commands/conftest.py

В модуле размещена фикстура <b>stop_api_before_test</b>, которая обеспечивает остановку приложения до 
выполнения и после выполнения <b>тестового кейса</b>, что позволяет избежать неожиданного поведения приложения, а также обеспечивает возвращение 
к состоянию до теста. Setup и teardown реализованы за счет использования ключевого слова `yield`.

```python
@pytest.fixture(autouse=True)
def stop_api_before_test():
    stop_api()
    yield
    stop_api()
```

### 3.2 test_commands/test_commands.py

В модуле реализованы тестовые функции:
- test_start_api - тестирование старта приложения;
- test_stop_api - тестирование остановки приложения;
- test_restart_api  - тестирование перезапуска приложения.


Все функции параметризованы списком кортежей URLS, который объявлен в "test_commands/utils.py" и 
имеет вид (host: str | None, port: str | None). Таким образом обеспечена возможность запуска 
приложения без дополнительных аргументов, с аргументом host, с аргументами host и port.

```python
URLS = [
    (),
    ('127.31.255.255', ),
    ('localhost', '5413'),
]
```

### 3.3 test_commands/test_state.py

В модуле реализованы тестовые функции:
- test_state_activate_server - тестирование задачи state c включенным сервером;
- test_state_disable_server - тестирование задачи state c выключенным сервером.

Также параметризованы списком URLS.


## 4. test_operations

Директория содержит:

- conftest.py - для размещения фикстуры <b>stop_api_before_test</b>;
- test_additions.py - тестовый модуль сложения;
- test_division.py - тестовый модуль деления;
- test_multiplication.py - тестовый модуль умножения;
- test_remainder.py - тестовый модуль вычисления остатка от деления;
- utils.py - для размещения дополнительной логики используемой в тестах директории test_operations.

### 4.1 test_operations/conftest.py

Реализована фикстура как и в "test_commands/conftest.py", но с указанием `scope='module'`. 
Это позволяет останавливать приложение до и после выполнения всего тестового модуля.


### 4.2 test_operations/utils.py

В данном модуле объявлены переменные и функции, которые могут использоваться всеми тестовыми модулями 
в каталоге "tests/test_operations". Переменные объявлены для дальнейшей параметризации функций
(аргументы некорректного типа данных, аргументы с превышением доступного лимита и т.д.). 
Переменные для параметризации, которые необходимы для определенной задачи, объявлены в соответствующих 
тестовых модулях.

Переменные для параметризации:

- HOST, PORT - все тестовые модули запускаются на сервере с адресом указанного в этих переменных;
- PARAMS_MISSING_ARGS - набор json данных с некорректными ключами;
- PARAMS_INCORRECT_TYPE - набор json данных с некорректным типом данных параметров;
- PARAMS_INCORRECT_LIMITS - набор json данных с параметрами превышающих установленный лимит;
- PARAMS_ZERO_DIVISION - набор json данных с делителем 0;
- DISABLE_SERVER_URLS - набор адресов формата (host: str, port: str) для тестирования запроса 
операции на выключенном сервере.

Функции используется для подготовки к тестированию:

 - preparation_for_test() - получение результата вычисления требуемой операции;
 
Если сервер неактивен, запускает его с указанными настройками и отправляет POST запрос с требуемой операций 
('api/addition', 'api/division', 'api/multiplication', 'api/remainder'). Возвращает json полученного ответа от сервера.

 - get_result_dis_server() - запрос результата вычисления на выключенном сервере.

Останавливает приложение и отправляет POST запрос с требуемой операций. Ожидается вызов исключения 
`ConnectionError(f"Сервер недоступен")`.


### 4.3 test_operations/test_addition.py

Переменные для параметризации:
- ADDITION_PARAMS_GOOD - аргументы для тестирования правильности вычисления сложения;
- ADDITION_INCORRECT_URLS - аргументы для тестирования ответа с некорректным телом запроса.

Тестовые функции:
- test_addition_good() - проверка правильности вычисляемого результата;
- test_addition_not_enough_keys() - проверка на возврат кода ошибки при неправильном указании параметров;
- test_addition_incorrect_data() - проверка на возврат кода ошибки при неправильном указании типов данных параметров;
- test_addition_limits() - проверка на возврат кода ошибки при превышении допустимых значений параметров;
- test_addition_incorrect_url() - проверка на возврат кода ошибки при неправильном формате тела запроса;
- test_add_try_operation_dis_server() - проверка на вызов исключения при отправке запроса на неактивный сервер.


### 4.4 test_operations/test_divisions.py

Переменные для параметризации:
- DIV_PARAMS_GOOD - аргументы для тестирования правильности вычисления деления;
- DIV_INCORRECT_URLS - аргументы для тестирования ответа с некорректным телом запроса.

Тестовые функции:
- test_division_good() - проверка правильности вычисляемого результата;
- test_division_not_enough_keys() - проверка на возврат кода ошибки при неправильном указании параметров;
- test_division_incorrect_data() - проверка на возврат кода ошибки при неправильном указании типов данных параметров;
- test_division_limits() - проверка на возврат кода ошибки при превышении допустимых значений параметров;
- test_division_incorrect_url() - проверка на возврат кода ошибки при неправильном формате тела запроса;
- test_division_zero_div() - проверка на возврат кода ошибки при делении на ноль;
- test_div_try_operation_dis_server() - проверка на вызов исключения при отправке запроса на неактивный сервер.


### 4.5 test_operations/test_multiplication.py

Переменные для параметризации:
- MULTI_PARAMS_GOOD - аргументы для тестирования правильности вычисления умножения;
- MULTI_INCORRECT_URLS - аргументы для тестирования ответа с некорректным телом запроса.

Тестовые функции:
- test_multi_good() - проверка правильности вычисляемого результата;
- test_multi_not_enough_keys() - проверка на возврат кода ошибки при неправильном указании параметров;
- test_multi_incorrect_data() - проверка на возврат кода ошибки при неправильном указании типов данных параметров;
- test_multi_limits() - проверка на возврат кода ошибки при превышении допустимых значений параметров;
- test_multi_incorrect_url() - проверка на возврат кода ошибки при неправильном формате тела запроса;
- test_multi_try_operation_dis_server() - проверка на вызов исключения при отправке запроса на неактивный сервер.

### 4.6 test_operations/test_remainder.py

Переменные для параметризации:
- REMAINDER_PARAMS_GOOD - аргументы для тестирования правильности вычисления остатка от деления;
- REMAINDER_INCORRECT_URLS - аргументы для тестирования ответа с некорректным телом запроса.

Тестовые функции:
- test_remainder_good() - проверка правильности вычисляемого результата;
- test_remainder_not_enough_keys() - проверка на возврат кода ошибки при неправильном указании параметров;
- test_remainder_incorrect_data() - проверка на возврат кода ошибки при неправильном указании типов данных параметров;
- test_remainder_limits() - проверка на возврат кода ошибки при превышении допустимых значений параметров;
- test_remainder_incorrect_url() - проверка на возврат кода ошибки при неправильном формате тела запроса;
- test_remainder_zero_div() - проверка на возврат кода ошибки при делении на ноль;
- test_rem_try_operation_dis_server() - проверка на вызов исключения при отправке запроса на неактивный сервер.


## 5. Журнал результатов тестирования

При запуске модуля <b>main.py</b> данные вывода записываются в файл формата 'txt' в директорию: 

<b>'./logs/дата теста в формате: число-месяц-год'</b>

Имя файла имеет следующий формат:

`test[номер теста на текущий день]_[тип теста]([время теста: часы-минуты])-[результат тестирования].txt`

Для демонстрации формата журналов было проведено несколько тестов 
(в одном из них алгоритм был намеренно изменен для ожидаемого провала).

Сформированные журналы можно посмотреть в директории <b>'./logs/07-08-2022'</b>
