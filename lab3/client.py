import socket
import json

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port

    def send_command(self, action, params=None):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                command = {"action": action}
                if params:
                    command["params"] = params
                client_socket.sendall(json.dumps(command).encode('utf-8'))
                response = client_socket.recv(4096).decode('utf-8')
                return json.loads(response)
        except ConnectionError as e:
            print(f"Connection error: {e}")
            return None

if __name__ == "__main__":
    client = Client(host='localhost', port=12345)

    print(client.send_command("updateBrand", {"id": 3, "is_flagship": True}))

    print(client.send_command("addManufacturer", {"id": 4, "name": "Toyota Motor Corporation"}))

    print(client.send_command("addBrand", {"id": 7, "name": "Toyota", "is_flagship": True, "model_count": 50, "manufacturer_id": 4}))
    print(client.send_command("addBrand", {"id": 8, "name": "Lexus", "is_flagship": False, "model_count": 40, "manufacturer_id": 4}))

    print(client.send_command("deleteBrand", {"id": 6}))

    print(client.send_command("showManufacturers"))

    print(client.send_command("showManufacturerBrands", {"manufacturer_id": 1}))


