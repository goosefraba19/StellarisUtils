import json, zipfile

from ..parse import Parser

from .country import Country
from .planet import Planet
from .pop import Pop
from .species import Species
from .starbase import Starbase
from .system import System

class Model:

    @staticmethod
    def from_file(path):
        if path.endswith(".sav"):
            return Model.from_savefile(path)
        elif path.endswith(".zip"):
            return Model.from_jsonzip(path)
        else:
            raise Exception("unrecognized file type")

    @staticmethod
    def from_savefile(path):
        parser = Parser()
        
        archive = zipfile.ZipFile(path)
        with archive.open("gamestate") as file:
            data = file.read().decode("utf-8")
            parser.input(data)

        obj = parser.parse()
        return Model(obj)

    @staticmethod
    def from_jsonzip(path):
        archive = zipfile.ZipFile(path)
        with archive.open("gamestate.json") as file:
            return Model(json.load(file))

    def __init__(self, obj):

        self.date = obj["date"]

        # create countries
        self.countries = dict([(k, Country(k,v)) for k,v in obj["country"].items() if v != "none"])

        # create systems
        self.systems = dict([(k, System(k,v)) for k,v in obj["galactic_object"].items()])
    
        # create starbases
        self.starbases = dict([(k, Starbase(k,v)) for k,v in obj["starbases"].items() if v != "none"])

        # link systems and starbases
        for starbase in self.starbases.values():
            system = self.systems[starbase.system_id]
            system.starbase = starbase
            starbase.system = system
            del starbase.system_id

        # link countries and starbases
        for country in self.countries.values():
            country.starbases = []
        for starbase in self.starbases.values():
            owner = self.countries[starbase.owner_id]
            owner.starbases.append(starbase)
            starbase.owner = owner
            del starbase.owner_id

        # create planets
        self.planets = dict([(k, Planet(k,v)) for k,v in obj["planet"].items() if v != "none"])

        # link systems and planets
        for system in self.systems.values():
            system.planets = [self.planets[x] for x in system.planet_ids]
            for planet in system.planets:
                planet.system = system
            del system.planet_ids

        # link countries and planets
        for country in self.countries.values():
            country.owned_planets = []
            country.controlled_planets = []
        for planet in self.planets.values():
            if planet.owner_id:
                planet.owner = self.countries[planet.owner_id]
                planet.owner.owned_planets.append(planet)
            else:
                planet.owner = None
                
            if planet.controller_id:
                planet.controller = self.countries[planet.controller_id]
                planet.controller.controlled_planets.append(planet)
            else:
                planet.controller = None

            del planet.owner_id
            del planet.controller_id

        # create pops
        self.pops = dict([(k, Pop(k,v)) for k,v in obj["pop"].items() if v != "none"])

        # link planets and pops
        for planet in self.planets.values():
            planet.pops = [self.pops[x] for x in planet.pop_ids]
            for pop in planet.pops:
                pop.planet = planet
            del planet.pop_ids

        # create species
        self.species = dict([(str(i), Species(str(i), v)) for (i,v) in enumerate(obj["species"])])

        # link species to each other
        for species in self.species.values():
            species.children = []
        for species in self.species.values():
            if species.parent_id:
                parent = self.species[species.parent_id]
                species.parent = parent
                parent.children.append(species)
            else:
                species.parent = None
            del species.parent_id

        # link species and pops
        for species in self.species.values():
            species.pops = []
        for pop in self.pops.values():
            species = self.species[pop.species_id]
            species.pops.append(pop)
            pop.species = species
            del pop.species_id
