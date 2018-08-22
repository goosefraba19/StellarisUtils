class Fleet:
    def __init__(self, id, value):
        self.id = id

        if "name" in value:
            self.name = value["name"]
        else:
            self.name = None

        self.is_civilian = "civilian" in value and value["civilian"] == "yes"
        self.is_station = "station" in value and value["station"] == "yes"

        self.ships = None
        self.owner = None

        if "owner" in value:
            self.owner_id = value["owner"]
        else:
            self.owner_id = None

    def __str__(self):
        return f"Fleet({self.id},name={self.name})"