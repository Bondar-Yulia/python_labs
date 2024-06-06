import pymqi
import time

# Параметри з'єднання
queue_manager = 'QM1'
channel = 'SVRCONN.1'
host = 'localhost'
port = '1414'
conn_info = f'{host}({port})'

# Налаштування черг
qmgr = pymqi.connect(queue_manager, channel, conn_info)
srv_queue = pymqi.Queue(qmgr, 'SRV.Q')
cl_queue = pymqi.Queue(qmgr, 'CL.Q')

# Відправка запиту
def send_request(request):
    srv_queue.put(request.encode('utf-8'))

# Отримання відповіді
def get_response():
    try:
        response = cl_queue.get(wait=3000).decode('utf-8')
        print(f'Отримано відповідь: {response}')
        return response
    except pymqi.MQMIError as e:
        print(f'Помилка: {e}')
        return None

# Приклад відправки запитів та отримання відповідей
def main():
    send_request('GET_MANUFACTURERS')
    time.sleep(1)  # Затримка для очікування відповіді
    response = get_response()
    if response:
        manufacturers = response.split(',')
        print(f'Виробники: {manufacturers}')

        for manufacturer in manufacturers:
            send_request(f'GET_BRANDS_FOR_MANUFACTURER:{manufacturer}')
            time.sleep(1)  # Затримка для очікування відповіді
            response = get_response()
            if response:
                brands = response.split(',')
                print(f'Марки для {manufacturer}: {brands}')

# Запуск клієнта
if __name__ == '__main__':
    main()

srv_queue.close()
cl_queue.close()
qmgr.disconnect()
