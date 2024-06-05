import Pyro4

uri = "PYRONAME:dealer.database"
dealer = Pyro4.Proxy(uri)

if __name__ == "__main__":
    try:
        dealer.updateBrand(3, True)
        dealer.addManufacturer(4, "Toyota Motor Corporation")
        dealer.addBrand(7, "Toyota", True, 50, 4)
        dealer.addBrand(8, "Lexus", False, 40, 4)
        dealer.deleteBrand(6)
        dealer.showManufacturers()
        dealer.showManufacturerBrands(1)
    except Pyro4.errors.CommunicationError as e:
        print("Error communicating with Pyro4 server:", e)
    finally:
        dealer.closeDB()

