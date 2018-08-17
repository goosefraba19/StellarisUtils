class Species:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]
        
        self.pops = None

    def __str__(self):
        return f"Species({self.id},name={self.name})"