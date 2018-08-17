class Species:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]

        self.parent = None
        self.children = None
        self.pops = None

        if "base" in value:
            self.parent_id = value["base"]
        else:
            self.parent_id = None

    def __str__(self):
        return f"Species({self.id},name={self.name})"