from dealer import Dealer

dealer = Dealer()
dealer.loadFromFile('dealer.xml')
dealer.showManufacturers()

for manufacturer in dealer.manufacturers:
    print(f"\nBrands for Manufacturer {manufacturer.id}, {manufacturer.name}:")
    dealer.showManufacturerBrands(manufacturer.id)

dealer.addManufacturer("m4", "BMW Motors")

dealer.modifyManufacturer("m4", "Toyota Motor Corporation")

dealer.addBrand("b7", "Toyota", True, 50, "m4")
dealer.addBrand("b8", "Lexus", False, 40, "m4")


dealer.modifyBrand("b3", "Porsche", True, 35)

print("\nAfter Modifications:")
print("Manufacturers:")
dealer.showManufacturers()

for manufacturer in dealer.manufacturers:
    print(f"\nBrands for Manufacturer {manufacturer.id}, {manufacturer.name}:")
    dealer.showManufacturerBrands(manufacturer.id)

dealer.saveToFile("updated_dealer.xml")
