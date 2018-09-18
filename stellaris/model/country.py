from .utils import getitem_or_default

class Country:
    def __init__(self, id, value):
        self.id = id

        self.type = getitem_or_default(value, "type", None)
        self.name = getitem_or_default(value, "name", None)
        self.adjective = getitem_or_default(value, "adjective", None) 

        if "flag" in value:
            self.flag = Flag(value["flag"])
        else:
            self.flag = None

        self.city_graphical_culture = getitem_or_default(value, "city_graphical_culture", None)
        self.graphical_culture = getitem_or_default(value, "graphical_culture", None)
        self.room = getitem_or_default(value, "room", None)
        self.name_list = getitem_or_default(value, "name_list", None)
        self.ship_prefix = getitem_or_default(value, "ship_prefix", None)

        self.ethos = getitem_or_default(value, "ethos", { "ethic": [] })["ethic"]
        self.policies = dict([(x["policy"], x["selected"]) for x in getitem_or_default(value, "active_policies", [])])
        self.edicts = set([x["edict"] for x in getitem_or_default(value, "edicts", [])])
        self.ascension_perks = getitem_or_default(value, "ascension_perks", [])
        self.traditions = getitem_or_default(value, "traditions", [])

        government = getitem_or_default(value, "government", None)
        if government != None:
            date = getitem_or_default(value, "government_date", None)
            self.government = Government(government, date)
        else:
            self.government = None

        self.personality = getitem_or_default(value, "personality", None)

        self.hyperlane_system_ids = set(getitem_or_default(value, "hyperlane_systems", []))
        self.restricted_system_ids = set(getitem_or_default(value, "restricted_systems", []))

        self.military_power = float(getitem_or_default(value, "military_power", 0))
        self.fleet_size = float(getitem_or_default(value, "fleet_size", 0))
        self.power_score = float(getitem_or_default(value, "power_score", 0))

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
        else:
            self.resources = None

        self.auto_ship_designs = getitem_or_default(value, "auto_ship_designs", "yes") == "yes"
        self.crisis_fighter = getitem_or_default(value, "crisis_fighter", "no") == "yes"
        self.starvation = getitem_or_default(value, "starvation", "no") == "yes"

        self.decedance = float(getitem_or_default(value, "decadence", 0))
        self.subject_type = getitem_or_default(value, "subject_type", None)



        # relationships

        self.owned_planets = []
        self.controlled_planets = []
        self.starbases = []
        self.factions = []
        self.leaders = []
        self.ruler = None
        self.fleets = []
        self.alliance = None
        self.associated_alliance = None
        self.capital = None
        self.overlord = None
        self.subjects = []

        self.ruler_id = getitem_or_default(value, "ruler", None)
        self.associated_alliance_id = getitem_or_default(value, "associated_alliance", None)
        self.capital_id = getitem_or_default(value, "capital", None)
        self.overlord_id = getitem_or_default(value, "overlord", None)
        self.ship_design_ids = getitem_or_default(value, "ship_design", [])

    def __str__(self):
        return f"Country({self.id},name={self.name})"



class Flag:
    def __init__(self, value):
        self.icon = value["icon"]
        self.background = value["background"]
        self.colors = [c for c in value["colors"] if c != "null"]



class Government:
    def __init__(self, value, date):
        self.type = value["type"]
        self.authority = value["authority"]
        self.civics = value["civics"]
        self.date = date