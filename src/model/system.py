from .utils import getitem_or_default

class System:
    def __init__(self, id, value):

        self.id = id
        self.name = value["name"]
        self.pos = (float(value["coordinate"]["x"]), float(value["coordinate"]["y"]))
        self.hyperlanes = [Hyperlane(self.id, x["to"], float(x["length"])) for x in getitem_or_default(value, "hyperlane", [])]



        # relationships

        self.planets = None
        self.starbase = None

        self.planet_ids = getitem_or_default(value, "planet", [])

    def __str__(self):
        return f"System({self.id},name={self.name})"



class Hyperlane:
    def __init__(self, src, dest, length):
        self.src = src
        self.dest = dest
        self.length = length
