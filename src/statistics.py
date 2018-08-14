import csv, os
from collections import Counter

def export_counters(settings, filename, counters):
    keys = set([])
    for counter in counters:
        for key in counter.keys():
            keys.add(key)
    keys = list(sorted(keys))

    folder_path = os.path.join(settings["output_folder_path"], settings["current"])

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    path = os.path.join(folder_path, filename)

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

    def step(self, model):
        species_pops = Counter()
        faction_pops = Counter()

        for planet in model.countries[self._id].planets:
            for pop in planet.pops:
                species_pops[pop.species.name] += 1
                if pop.ethic:
                    faction_pops[pop.ethic] += 1

        self._species_pops.append(species_pops)
        self._faction_pops.append(faction_pops)

    def export(self, settings):
        export_counters(settings, self._name + "_species_pops.csv", self._species_pops)
        export_counters(settings, self._name + "_faction_pops.csv", self._faction_pops)



class SpeciesCounts:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._country_pops = []

    def step(self, model):
        pop_country = Counter()

        for pop in model.pops.values():
            if pop.species.id == self._id and pop.planet.country != None:
                pop_country[pop.planet.country.name] += 1

        self._country_pops.append(pop_country)

    def export(self, settings):
        export_counters(settings, self._name + "_country_pops.csv", self._country_pops)



class GalaxyCounts:
    def __init__(self):
        self._species_pops = []
        self._country_pops = []
        self._country_planets = []
    
    def step(self, model):
        species_pops = Counter()
        country_pops = Counter()
        country_planets = Counter()

        for pop in model.pops.values():
            species_pops[pop.species.name] += 1
            if pop.planet != None and pop.planet.country != None:
                country_pops[pop.planet.country.name] += 1
            else:
                country_pops["none"] += 1
				
        for planet in model.planets.values():
            if planet.is_habitable:
                if planet.country != None:
                    country_planets[planet.country.name] += 1
                else:
                    country_planets["none"] += 1

        self._species_pops.append(species_pops)
        self._country_pops.append(country_pops)
        self._country_planets.append(country_planets)

    def export(self, settings):
        export_counters(settings, "galaxy_species_pops.csv", self._species_pops)
        export_counters(settings, "galaxy_country_pops.csv", self._country_pops)
        export_counters(settings, "galaxy_country_planets.csv", self._country_planets)
