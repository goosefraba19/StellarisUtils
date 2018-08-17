class Hyperlane:
    def __init__(self, src, dest, length):
        self.src = src
        self.dest = dest
        self.length = length

keys = set()

class System:
    def __init__(self, id, value):

        self.id = id
        self.name = value["name"]
        self.pos = (float(value["coordinate"]["x"]), float(value["coordinate"]["y"]))

        if "hyperlane" in value:
            self.hyperlanes = [Hyperlane(self.id, x["to"], float(x["length"])) for x in value["hyperlane"]]
        else:
            self.hyperlanes = []

        self.planets = None
        self.starbase = None

        if "planet" in value:
            self.planet_ids = value["planet"]
        else:
            self.planet_ids = []

    def __str__(self):
        return f"System({self.id},name={self.name})"