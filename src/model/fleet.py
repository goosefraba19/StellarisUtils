from .utils import getitem_or_default

class Fleet:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)
        self.is_civilian = getitem_or_default(value, "civilian", "no") == "yes"
        self.is_station = getitem_or_default(value, "station", "no") == "yes"



        # relationships

        self.ships = []
        self.owner = None

        self.owner_id = getitem_or_default(value, "owner", None)

    def __str__(self):
        return f"Fleet({self.id},name={self.name})"