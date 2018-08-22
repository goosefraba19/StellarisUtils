class ShipDesign:
    def __init__(self, id, value):
        self.id = id

        if "name" in value:
            self.name = value["name"]
        else:
            self.name = None

        self.size = value["ship_size"]

    def __str__(self):
        return f"ShipDesign({self.id},name={self.name})"