class Pop:
    def __init__(self, id, value):
        self.id = id

        if "ethos" in value:
            self.ethic = value["ethos"]["ethic"]
        else:
            self.ethic = None

        if "enslaved" in value:
            self.enslaved = True
        else:
            self.enslaved = False

        self.planet = None
        self.species = None

        self.species_id = value["species_index"]

    def __str__(self):
        return f"Pop({self.id})"