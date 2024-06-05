import MySQLdb
from MySQLdb import Error
import socket
import json

class DealerDatabase:
    def __init__(self):
        self.db = self.connectDB()

    def connectDB(self):
        try:
            db = MySQLdb.connect(
                host="localhost",
                user="root",
                password="password",
                database="DEALER"
            )
            return db
        except Error as e:
            print(f"Error: {e}")
            return None

    def addBrand(self, id, name, is_flagship, model_count, manufacturer_id):
        if self.db is None:
            return False

        sql = "INSERT INTO BRANDS (ID_BR, NAME, IS_FLAGSHIP, MODEL_COUNT, ID_MF) VALUES (%s, %s, %s, %s, %s)"
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (id, name, is_flagship, model_count, manufacturer_id))  # Use parameterized queries
            self.db.commit()
            print(f"Brand {name} successfully added")
            return True
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def addManufacturer(self, id, name):
        if self.db is None:
            return False

        sql = "INSERT INTO MANUFACTURERS (ID_MF, NAME) VALUES (%s, %s)"
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (id, name))  # Use parameterized queries
            self.db.commit()
            print(f"Manufacturer {name} successfully added")
            return True
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def updateBrand(self, id, name=None, is_flagship=None, model_count=None):
        if self.db is None:
            return False

        updates = []
        params = []

        if name is not None:
            updates.append("NAME = %s")
            params.append(name)
        if is_flagship is not None:
            updates.append("IS_FLAGSHIP = %s")
            params.append(is_flagship)
        if model_count is not None:
            updates.append("MODEL_COUNT = %s")
            params.append(model_count)

        if not updates:
            print("No fields to update")
            return False

        sql = f"UPDATE BRANDS SET {', '.join(updates)} WHERE ID_BR = %s"
        params.append(id)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql, params)
            self.db.commit()
            print(f"Brand with ID {id} successfully updated")
            return True
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def updateManufacturer(self, id, name=None):
        if self.db is None:
            return False

        updates = []
        params = []

        if name is not None:
            updates.append("NAME = %s")
            params.append(name)

        if not updates:
            print("No fields to update")
            return False

        sql = f"UPDATE MANUFACTURERS SET {', '.join(updates)} WHERE ID_MF = %s"
        params.append(id)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql, params)
            self.db.commit()
            print(f"Manufacturer with ID {id} successfully updated")
            return True
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def deleteBrand(self, id):
        if self.db is None:
            return False

        sql = "DELETE FROM BRANDS WHERE ID_BR = %s"
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (id,))
            self.db.commit()
            print(f"Brand with ID {id} successfully deleted")
            return True
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()


    def deleteManufacturer(self, id):
        if self.db is None:
            return False    
        
        sql = "DELETE FROM MANUFACTURERS WHERE ID_MF = %s"

        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (id,))
            self.db.commit()
            print(f"Manufacturer with ID {id} successfully deleted")
            return True
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def showManufacturers(self):
        if self.db is None:
            return False

        sql = "SELECT * FROM MANUFACTURERS"

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            manufacturers = cursor.fetchall()
            for manufacturer in manufacturers:
                print(manufacturer)
            return manufacturers
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def showManufacturerBrands(self, manufacturer_id):
        if self.db is None:
            return False

        sql = "SELECT * FROM BRANDS WHERE ID_MF = %s"
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (manufacturer_id,))
            brands = cursor.fetchall()
            for brand in brands:
                print(brand)
            return brands
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def closeDB(self):  
        if self.db is not None:
            self.db.close()
            print("Database connection closed")

class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database = DealerDatabase()

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started at {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)


    def handle_client(self, client_socket):
        with client_socket as sock:
            request = sock.recv(1024).decode('utf-8')
            response = self.process_request(request)
            sock.sendall(response.encode('utf-8'))

    def process_request(self, request):
        try:
            request_data = json.loads(request)
            action = request_data.get("action")
            params = request_data.get("params", {})
            
            if action == "addBrand":
                result = self.database.addBrand(**params)
            elif action == "addManufacturer":
                result = self.database.addManufacturer(**params)
            elif action == "updateBrand":
                result = self.database.updateBrand(**params)
            elif action == "updateManufacturer":
                result = self.database.updateManufacturer(**params)
            elif action == "deleteBrand":
                result = self.database.deleteBrand(params["id"])
            elif action == "deleteManufacturer":
                result = self.database.deleteManufacturer(params["id"])
            elif action == "showManufacturers":
                result = self.database.showManufacturers()
            elif action == "showManufacturerBrands":
                result = self.database.showManufacturerBrands(params["manufacturer_id"])
            else:
                return json.dumps({"error": "Invalid action"})

            return json.dumps({"result": result})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def stop_server(self):
        self.database.closeDB()
        self.server_socket.close()
        print("Server stopped")

if __name__ == "__main__":  
    server = Server()
    server.start_server()
    server.stop_server()