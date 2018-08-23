from .utils import getitem_or_default

PLANET_CLASS_HABITABLE = set([
    # Dry
    "pc_desert",
    "pc_arid",
    "pc_savannah",
    # Wet
    "pc_tropical",
    "pc_continental",
    "pc_ocean",
    # Cold
    "pc_tundra",
    "pc_arctic",
    "pc_alpine",
    # Other
    "pc_gaia",
    "pc_tomb",
    "pc_machine",
    "pc_habitat",
    "pc_ringworld_habitable"
])

class Planet:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)
        self.size = int(getitem_or_default(value, "planet_size", 0))
        self.type = getitem_or_default(value, "planet_class", None)
        self.is_habitable = self.type in PLANET_CLASS_HABITABLE 



        # relationships

        self.owner = None
        self.controller = None
        self.pops = None
        self.system = None

        self.owner_id = getitem_or_default(value, "owner", None)
        self.controller_id = getitem_or_default(value, "controller", None)
        self.pop_ids = getitem_or_default(value, "pop", [])

    def __str__(self):
        return f"Planet({self.id},name={self.name},type={self.type})"