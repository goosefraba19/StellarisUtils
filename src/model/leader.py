from .utils import getitem_or_default

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

        self.gender = getitem_or_default(value, "gender", None)

        self.role = value["class"]
        self.level = int(value["level"])



        # relationships

        self.species = None
        self.country = None

        self.species_index = int(value["species_index"])
        self.country_id = value["country"]

    def __str__(self):
        return f"Leader({self.id},name={self.name})"
