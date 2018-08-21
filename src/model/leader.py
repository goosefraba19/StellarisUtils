class Leader:
    def __init__(self, id, value):
        self.id = id

        if "name" in value:
            name = value["name"]
            first = name["first_name"]
            if "second_name" in name:
                second = name["second_name"]
                self.name = f"{first} {second}"
            else:
                self.name = first
        else:
            self.name = None

        if "gender" in value:
            self.gender = value["gender"]
        else:
            self.gender = None

        self.role = value["class"]
        self.level = int(value["level"])

        self.species = None
        self.country = None

        self.species_index = int(value["species_index"])
        self.country_id = value["country"]

    def __str__(self):
        return f"Leader({self.id},name={self.name})"
