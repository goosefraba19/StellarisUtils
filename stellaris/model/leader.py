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

        self.portrait = getitem_or_default(value, "portrait", None)
        self.gender = getitem_or_default(value, "gender", None)
        self.age = int(getitem_or_default(value, "age", 0))

        self.level = int(getitem_or_default(value, "level", 0))
        self.experience = float(getitem_or_default(value, "experience", 0.0))

        self.role = getitem_or_default(value, "class", None)
        self.agenda = getitem_or_default(value, "agenda", None)

        self.traits = []
        if "roles" in value:
            role = value["roles"][self.role]
            if "traits" in role:
                self.traits = role["traits"]

        self.mandate = None
        if "mandate" in value:
            self.mandate = value["mandate"]["type"]



        # relationships

        self.species = None
        self.country = None

        self.species_index = int(value["species_index"])
        self.country_id = getitem_or_default(value, "country", None)

    def __str__(self):
        return f"Leader({self.id},name={self.name})"
