from .utils import getitem_or_default

class Starbase:
    def __init__(self, id, value):
        self.id = id
        self.level = getitem_or_default(value, "level", None)



        # relationships

        self.owner = None
        self.system = None

        self.owner_id = value["owner"]
        self.system_id = value["system"]

    def __str__(self):
        return f"Starbase({self.id})"