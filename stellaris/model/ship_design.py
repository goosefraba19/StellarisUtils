from .utils import getitem_or_default

class ShipDesign:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)
        self.size = getitem_or_default(value, "ship_size", None)

    def __str__(self):
        return f"ShipDesign({self.id},name={self.name})"