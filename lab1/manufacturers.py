class Manufacturer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Brand:
    def __init__(self, id, name, is_flagship, model_count, manufacturer):
        self.id = id
        self.name = name
        self.is_flagship = is_flagship
        self.model_count = model_count
        self.manufacturer = manufacturer