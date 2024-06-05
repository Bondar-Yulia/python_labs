import xml.dom.minidom as minidom
from lxml import etree
from manufacturers import Manufacturer, Brand

class Dealer:
    def __init__(self):
        self.manufacturers = []
        self.brands = []

    def getManufacturer(self, id):
        for manufacturer in self.manufacturers:
            if manufacturer.id == id:
                return manufacturer
        raise Exception(f"Manufacturer with id {id} not found")

    def getBrand(self, id):
        for brand in self.brands:
            if brand.id == id:
                return brand
        raise Exception(f"Brand with id {id} not found")

    def addManufacturer(self, id, name):
        if any(manufacturer.id == id for manufacturer in self.manufacturers):
            raise Exception(f"Manufacturer with id {id} already exists")
        self.manufacturers.append(Manufacturer(id, name))

    def addBrand(self, id, name, is_flagship, model_count, manufacturer_id):
        if any(brand.id == id for brand in self.brands):
            raise Exception(f"Brand with id {id} already exists")
        manufacturer = self.getManufacturer(manufacturer_id)
        self.brands.append(Brand(id, name, is_flagship, model_count, manufacturer))

    def modifyManufacturer(self, id, name):
        manufacturer = self.getManufacturer(id)
        manufacturer.name = name

    def modifyBrand(self, id, name, is_flagship, model_count):
        brand = self.getBrand(id)
        brand.name = name
        brand.is_flagship = is_flagship
        brand.model_count = model_count

    def deleteManufacturer(self, id):
        manufacturer = self.getManufacturer(id)
        self.manufacturers.remove(manufacturer)
        self.brands = [brand for brand in self.brands if brand.manufacturer.id != id]

    def deleteBrand(self, id):
        brand = self.getBrand(id)
        self.brands.remove(brand)

    def saveToFile(self, filename):
        doc = minidom.Document()
        dealer = doc.createElement('Dealer')
        doc.appendChild(dealer)

        for manufacturer in self.manufacturers:
            manufacturer_elem = doc.createElement("Manufacturer")
            manufacturer_elem.setAttribute("id", manufacturer.id)
            manufacturer_elem.setAttribute("name", manufacturer.name)
            dealer.appendChild(manufacturer_elem)

            for brand in self.brands:
                if brand.manufacturer == manufacturer:
                    brand_elem = doc.createElement("Brand")
                    brand_elem.setAttribute("id", brand.id)
                    brand_elem.setAttribute("name", brand.name)
                    brand_elem.setAttribute("is_flagship", "1" if brand.is_flagship else "0")
                    brand_elem.setAttribute("model_count", str(brand.model_count))
                    manufacturer_elem.appendChild(brand_elem)

        xml_str = doc.toprettyxml(indent="\t")
        with open(filename, "w") as f:
            f.write(xml_str)

    def loadFromFile(self, filename):
        xml_validator = etree.XMLSchema(file="dealer.xsd")

        try:
            xml_file = etree.parse(filename)
        except etree.XMLSyntaxError as e:
            print(f"XML Syntax Error: {e}")
            return

        if not xml_validator.validate(xml_file):
            print("XML is not valid")
            return
   
        DOMTree = minidom.parse(filename)
        collection = DOMTree.documentElement

        manufacturers = collection.getElementsByTagName("Manufacturer")

        for manufacturer in manufacturers:
            id = manufacturer.getAttribute("id")
            name = manufacturer.getAttribute("name")
            man_obj = Manufacturer(id, name)
            self.manufacturers.append(man_obj)

            brands = manufacturer.getElementsByTagName("Brand")

            for brand in brands:
                id = brand.getAttribute("id")
                name = brand.getAttribute("name")
                is_flagship = brand.getAttribute("is_flagship") == '1'
                model_count = int(brand.getAttribute("model_count"))
                brand_obj = Brand(id, name, is_flagship, model_count, man_obj)
                self.brands.append(brand_obj)

    def showManufacturers(self):
        for manufacturer in self.manufacturers:
            print(f"Manufacturer: {manufacturer.id}, {manufacturer.name}")

    def showManufacturerBrands(self, manufacturer_id):
        manufacturer = self.getManufacturer(manufacturer_id)
        manufacturer_brands = [brand for brand in self.brands if brand.manufacturer == manufacturer]
        for brand in manufacturer_brands:
            print(f"Brand: {brand.id}, {brand.name}, Flagship: {brand.is_flagship}, Model Count: {brand.model_count}")
