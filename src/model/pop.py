from .utils import getitem_or_default

class Pop:
    def __init__(self, id, value):
        self.id = id
        self.ethic = getitem_or_default(value, "ethos", { "ethic": None })["ethic"]
        self.enslaved = getitem_or_default(value, "enslaved", "no") == "yes"



        # relationships

        self.planet = None
        self.species = None
        self.faction = None

        self.species_index = int(value["species_index"])

    def __str__(self):
        return f"Pop({self.id})"