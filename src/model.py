import json

class Hyperlane:
    def __init__(self, src, dest, length):
        self.src = src
        self.dest = dest
        self.length = length

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
        self.is_habitable = value["planet_class"] in PLANET_CLASS_HABITABLE 

        if "pop" in value:
            self.pop_ids = value["pop"]
        else:
            self.pop_ids = []

        self.country = None
        self.pops = None
        self.system = None

class Pop:
    def __init__(self, id, value):
        self.id = id
        self.species_id = value["species_index"]

        if "ethos" in value:
            self.ethic = value["ethos"]["ethic"]
        else:
            self.ethic = None

        self.planet = None
        self.species = None


class Starbase:
    def __init__(self, id, value):
        self.id = id
        self.country_id = value["owner"]

        self.country = None
        self.system = None

class System:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]
        self.pos = (float(value["coordinate"]["x"]), float(value["coordinate"]["y"]))

        if "hyperlane" in value:
            self.hyperlanes = [Hyperlane(self.id, x["to"], float(x["length"])) for x in value["hyperlane"]]
        else:
            self.hyperlanes = []

        if "planet" in value:
            self.planet_ids = value["planet"]
        else:
            self.planet_ids = []

        if "starbase" in value and value["starbase"] != "4294967295":
            self.starbase_id = value["starbase"]
        else:
            self.starbase_id = None

        self.planets = None
        self.starbase = None

class Country:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]
        self.flag = value["flag"]

        if "owned_planets" in value:
            self.planet_ids = value["owned_planets"]
        else:
            self.planet_ids = []

        self.planets = None
        self.starbases = None

class Species:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]
        
        self.pops = None


class Model:
    def __init__(self, path):
        with open(path, "r") as file:
            all_data = json.load(file)

            # create countries
            self.countries = dict([(k, Country(k,v)) for k,v in all_data["country"].items() if v != "none"])

            # create systems
            self.systems = dict([(k, System(k,v)) for k,v in all_data["galactic_object"].items()])
        
            # create starbases
            self.starbases = dict([(k, Starbase(k,v)) for k,v in all_data["starbases"].items() if v != "none"])

            # link systems and starbases
            for system in self.systems.values():
                if system.starbase_id != None and system.starbase_id in self.starbases:
                    starbase = self.starbases[system.starbase_id]
                    system.starbase = starbase
                    starbase.system = system
                del system.starbase_id

            # link countries and starbases
            for country in self.countries.values():
                country.starbases = []
            for starbase in self.starbases.values():
                country = self.countries[starbase.country_id]
                country.starbases.append(starbase)
                starbase.country = country
                del starbase.country_id

            # create planets
            self.planets = dict([(k, Planet(k,v)) for k,v in all_data["planet"].items() if v != "none"])

            # link systems and planets
            for system in self.systems.values():
                system.planets = [self.planets[x] for x in system.planet_ids]
                for planet in system.planets:
                    planet.system = system
                del system.planet_ids

            # link countries and planets
            for country in self.countries.values():
                country.planets = [self.planets[x] for x in country.planet_ids]
                for planet in country.planets:
                    planet.country = country
                del country.planet_ids

            # create pops
            self.pops = dict([(k, Pop(k,v)) for k,v in all_data["pop"].items() if v != "none"])

            # link planets and pops
            for planet in self.planets.values():
                planet.pops = [self.pops[x] for x in planet.pop_ids]
                for pop in planet.pops:
                    pop.planet = planet
                del planet.pop_ids

            # create species
            self.species = dict([(str(i), Species(str(i), v)) for (i,v) in enumerate(all_data["species"])])

            # link species and pops
            for species in self.species.values():
                species.pops = []
            for pop in self.pops.values():
                species = self.species[pop.species_id]
                species.pops.append(pop)
                pop.species = species
                del pop.species_id
