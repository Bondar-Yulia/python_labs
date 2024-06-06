import pymqi
import xml.etree.ElementTree as ET

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

# Завантаження даних з XML
tree = ET.parse('updated_dealer.xml')
root = tree.getroot()

# Обробка запитів
def process_request():
    try:
        request = srv_queue.get().decode('utf-8')
        response = handle_request(request)
        cl_queue.put(response.encode('utf-8'))
        return True
    except pymqi.MQMIError as e:
        print(f'Помилка: {e}')
        return False

def handle_request(request):
    if request == 'GET_MANUFACTURERS':
        return get_manufacturers()
    elif request.startswith('GET_BRANDS_FOR_MANUFACTURER:'):
        manufacturer_name = request.split(':')[1]
        return get_brands_for_manufacturer(manufacturer_name)
    else:
        return 'UNKNOWN_REQUEST'

def get_manufacturers():
    manufacturers = [manufacturer.get('name') for manufacturer in root.findall('Manufacturer')]
    return ','.join(manufacturers)

def get_brands_for_manufacturer(manufacturer_name):
    for manufacturer in root.findall('Manufacturer'):
        if manufacturer.get('name') == manufacturer_name:
            brands = [brand.get('name') for brand in manufacturer.findall('Brand')]
            return ','.join(brands)
    return 'MANUFACTURER_NOT_FOUND'

# Запуск сервера
while process_request():
    pass

srv_queue.close()
cl_queue.close()
qmgr.disconnect()
