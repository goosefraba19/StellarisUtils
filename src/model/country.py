class Country:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]
        self.flag = value["flag"]
        self.military_power = float(value["military_power"])
        self.fleet_size = float(value["fleet_size"])
        self.power_score = float(value["power_score"])

        self.resources = None
        if "standard_economy_module" in value["modules"]:
            self.resources = {}
            resources = value["modules"]["standard_economy_module"]["resources"]
            for k, v in resources.items():
                if type(v)==list:
                    self.resources[k] = list(map(float, v))
                elif type(v)==str:
                    self.resources[k] = [float(v), 0, 0]
                else:
                    raise Exception("unrecognized resource value")

        self.owned_planets = None
        self.controlled_planets = None
        self.starbases = None
        self.factions = None
        self.leaders = None
        self.ruler = None

        if "ruler" in value:
            self.ruler_id = value["ruler"]
        else:
            self.ruler_id = None

    def __str__(self):
        return f"Country({self.id},name={self.name})"