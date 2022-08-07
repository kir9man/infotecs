import os
import requests


# проверка активности сервера
def check_connect(host: str = '127.0.0.1', port: str = '17678'):
    try:
        response_status = requests.get(f"http://{host}:{port}" + "/api/state")
        return response_status.json()
    except:
        return {'statusCode': 1, 'statusMessage': f"Сервер {host}:{port} недоступен"}


# запуск приложения
def run_api(host: str = '127.0.0.1', port: str = '17678'):
    if check_connect(host, port)['statusCode']:
        os.system(f"webcalculator.exe start {host} {port}")


# остановка приложения
def stop_api():
    os.system("webcalculator.exe stop")


# перезапуск приложения
def restart_api(host: str = '127.0.0.1', port: str = '17678'):
    if not check_connect(host, port)['statusCode']:
        os.system("webcalculator.exe restart")
