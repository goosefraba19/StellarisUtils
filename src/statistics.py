import csv, os
from collections import Counter

from .files import get_output_folder_path


def export_counters(filename, counters):
    keys = set([])
    for counter in counters:
        for key in counter.keys():
            keys.add(key)
    keys = list(sorted(keys))

    output_folder_path = get_output_folder_path()

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    path = os.path.join(output_folder_path, filename)

    with open(path, "w", newline='') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()

        for counter in counters:
            writer.writerow(dict([(key, counter[key]) for key in keys]))



class CountryCounts:
    def __init__(self, id, name):
        self._id = id
        self._name = name

        self._species_pops = []
        self._faction_pops = []
        self._resources = []
        self._military = []

    def step(self, model):
        country = model.countries[self._id]

        species_pops = Counter()
        faction_pops = Counter()

        for planet in country.owned_planets:
            for pop in planet.pops:

                species = pop.species
                if species.base != None:
                    species = species.base
                species_pops[species.name] += 1

                if pop.faction and pop.faction in country.factions:
                    faction_pops[pop.faction.name] += 1

        resources = {}
        for key, value in country.resources.items():
            resources[key + "_total"] = value[0]
            resources[key + "_produced"] = value[1]
            resources[key + "_consumed"] = value[2]

        military = {
            "military_power": country.military_power,
            "fleet_size": country.fleet_size,
            "power_score": country.power_score
        }

        self._species_pops.append(species_pops)
        self._faction_pops.append(faction_pops)
        self._resources.append(resources)
        self._military.append(military)

    def export(self):
        export_counters(self._name + "_species_pops.csv", self._species_pops)
        export_counters(self._name + "_faction_pops.csv", self._faction_pops)
        export_counters(self._name + "_resources.csv", self._resources)
        export_counters(self._name + "_military.csv", self._military)



class SpeciesCounts:
    def __init__(self, ids, name, include_children=False):
        if type(ids) is not list:
            self._ids = [ids]
        else:
            self._ids = ids

        self._name = name
        self._country_pops = []
        self._include_children = include_children

    def step(self, model):
        country_pops = Counter()

        for pop in model.pops.values():
            if self._is_included(pop.species):
                if pop.planet.owner != None:
                    country_pops[pop.planet.owner.name] += 1
                else:
                    country_pops["none"] += 1

        self._country_pops.append(country_pops)
    
    def _is_included(self, species):
        if species.id in self._ids:
            return True
        elif self._include_children and species.base != None and species.base.id in self._ids:
            return True
        else:
            return False


    def export(self):
        export_counters(self._name + "_country_pops.csv", self._country_pops)



class GalaxyCounts:
    def __init__(self):
        self._species_pops = []
        self._country_pops = []
        self._country_planets = []
        self._scores = []
    
    def step(self, model):
        species_pops = Counter()
        country_pops = Counter()
        country_planets = Counter()
        scores = Counter()

        for pop in model.pops.values():

            species = pop.species
            if species.base != None:
                species = species.base
            species_pops[species.name] += 1

            if pop.planet != None and pop.planet.owner != None:
                country_pops[pop.planet.owner.name] += 1
            else:
                country_pops["none"] += 1
				
        for planet in model.planets.values():
            if planet.is_habitable:
                if planet.owner != None:
                    country_planets[planet.owner.name] += 1
                else:
                    country_planets["none"] += 1

        for country in model.countries.values():
            scores[country.name] = country.power_score

        self._species_pops.append(species_pops)
        self._country_pops.append(country_pops)
        self._country_planets.append(country_planets)
        self._scores.append(scores)

    def export(self):
        export_counters("galaxy_species_pops.csv", self._species_pops)
        export_counters("galaxy_country_pops.csv", self._country_pops)
        export_counters("galaxy_country_planets.csv", self._country_planets)
        export_counters("galaxy_score.csv", self._scores)
