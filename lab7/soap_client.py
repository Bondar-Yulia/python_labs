from zeep import Client

client = Client('http://127.0.0.1:8000/soap/?wsdl')
print('All manufacturers:', client.service.get_all_manufacturers())
print('Brands for Toyota:', client.service.get_brands_by_manufacturer('Toyota'))
