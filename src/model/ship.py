from .utils import getitem_or_default

class Ship:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)



        # relationships

        self.design = None
        self.fleet = None

        self.design_id = value["ship_design"]
        self.fleet_id = value["fleet"]