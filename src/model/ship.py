class Ship:
    def __init__(self, id, value):
        self.id = id

        if "name" in value:
            self.name = value["name"]
        else:
            self.name = None

        self.design = None
        self.fleet = None

        self.design_id = value["ship_design"]
        self.fleet_id = value["fleet"]