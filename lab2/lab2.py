import MySQLdb
from MySQLdb import Error

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

db = DealerDatabase()

db.updateBrand(3, is_flagship=True)

db.addManufacturer(4, "Toyota Motor Corporation")

db.addBrand(7, "Toyota", True, 50, 4)
db.addBrand(8, "Lexus", False, 40, 4)

db.deleteBrand(6)

db.showManufacturers()

db.showManufacturerBrands(1)

db.closeDB()