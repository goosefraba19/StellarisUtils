import json, zipfile

from ..parse import Parser

from .country import Country
from .faction import Faction
from .fleet import Fleet
from .leader import Leader
from .planet import Planet
from .pop import Pop
from .ship import Ship 
from .ship_design import ShipDesign
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
        species = [Species(v) for v in obj["species"]]
        self.species = dict([(s.id, s) for s in species])

        # link species to each other
        for s in species:
            s.children = []
        for s in species:
            if s.base_index != None:
                base = species[s.base_index]
                s.base = base
                base.children.append(s)
                del s.base_index

        # link species to pops
        for s in species:
            s.pops = []
        for pop in self.pops.values():
            s = species[pop.species_index]
            pop.species = s
            s.pops.append(pop)
            del pop.species_index

        # create factions
        if "pop_factions" in obj:
            self.factions = dict([(k, Faction(k,v)) for (k,v) in obj["pop_factions"].items() if v != "none"])
        else:
            self.factions = {}

        # link factions and countries
        for country in self.countries.values():
            country.factions = []
        for faction in self.factions.values():
            country = self.countries[faction.country_id]
            faction.country = country
            country.factions.append(faction)
            del faction.country_id

        # link factions and pops
        for faction in self.factions.values():
            faction.members = [self.pops[id] for id in faction.member_ids]
            for member in faction.members:
                member.faction = faction
            del faction.member_ids

        # create leaders
        self.leaders = dict([(k, Leader(k,v)) for k,v in obj["leaders"].items() if v != "none"])

        # ilnk leaders and species
        for s in species:
            s.leaders = []
        for leader in self.leaders.values():
            s = species[leader.species_index]
            leader.species = s
            s.leaders.append(leader)
            del leader.species_index

        # link leaders and countries
        for country in self.countries.values():
            country.leaders = []
        for leader in self.leaders.values():
            if leader.country_id in self.countries:
                country = self.countries[leader.country_id]
                leader.country = country
                country.leaders.append(leader)
            else:
                leader.country = None
            del leader.country_id

        for country in self.countries.values():
            if country.ruler_id:
                country.ruler = self.leaders[country.ruler_id]
            del country.ruler_id

        # link factions and leaders
        for faction in self.factions.values():
            if faction.leader_id in self.leaders:
                faction.leader = self.leaders[faction.leader_id]
            del faction.leader_id

        # create fleets
        fleets = []
        for k,v in obj["fleet"].items():
            if v == "none":
                continue
            if "killed" in v and v["killed"] == "yes":
                continue
            fleets.append((k, Fleet(k,v)))
        self.fleets = dict(fleets)

        # link fleets and countries
        for country in self.countries.values():
            country.fleets = []
        for fleet in self.fleets.values():
            if fleet.owner_id in self.countries:
                owner = self.countries[fleet.owner_id]
                fleet.owner = owner
                owner.fleets.append(fleet)
            del fleet.owner_id

        # create ship designs
        self.ship_designs = dict([(k, ShipDesign(k,v)) for k,v in obj["ship_design"].items() if v != "none"])

        # create ships
        self.ships = dict([(k, Ship(k,v)) for k,v in obj["ships"].items() if v != "none"])

        # link ships and ship designs
        for ship in self.ships.values():
            ship.design = self.ship_designs[ship.design_id]
            del ship.design_id

        # link ships and fleets
        for fleet in self.fleets.values():
            fleet.ships = []
        for ship in self.ships.values():
            if ship.fleet_id in self.fleets:
                fleet = self.fleets[ship.fleet_id]
                ship.fleet = fleet
                fleet.ships.append(ship)
            del ship.fleet_id


