from .utils import getitem_or_default

class System:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)
        self.pos = (float(value["coordinate"]["x"]), float(value["coordinate"]["y"]))
        self.hyperlanes = [Hyperlane(self, x["to"], float(x["length"])) for x in getitem_or_default(value, "hyperlane", [])]



        # relationships

        self.planets = None
        self.starbase = None

        if "planet" in value:
            ids = value["planet"]
            if type(ids) == list:
                self.planet_ids = ids
            elif type(ids) == str:
                self.planet_ids = [ids]
            else:
                raise Exception(f"Unrecognized type '{type(ids)}' for planet ids.")
        else:
            self.planet_ids = []

    def __str__(self):
        return f"System({self.id},name={self.name})"



class Hyperlane:
    def __init__(self, src, dest_id, length):
        self.src = src
        self.length = length

        # relationships
        self.dest = None

        self.dest_id = dest_id

    def __str__(self):
        return f"Hyperlane({self.src.id},{self.dest.id})"

    def __key(self):
        ids = list(sorted([self.src.id, self.dest.id]))
        return (ids[0], ids[1], self.length)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())
