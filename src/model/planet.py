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
        self.name = value["name"]
        self.size = int(value["planet_size"])
        self.type = value["planet_class"]
        self.is_habitable = value["planet_class"] in PLANET_CLASS_HABITABLE 

        self.owner = None
        self.controller = None
        self.pops = None
        self.system = None

        if "owner" in value:
            self.owner_id = value["owner"]
        else:
            self.owner_id = None

        if "controller" in value:
            self.controller_id = value["controller"]
        else:
            self.controller_id = None

        if "pop" in value:
            self.pop_ids = value["pop"]
        else:
            self.pop_ids = []

    def __str__(self):
        return f"Planet({self.id},name={self.name},type={self.type})"