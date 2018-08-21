import hashlib

class Species:
    def __init__(self, value):
        self.name = value["name"]

        if "trait" in value["traits"]:
            self.traits = value["traits"]["trait"]
        else:
            self.traits = []

        self._class = value["class"]
        self._portrait = value["portrait"]

        if "name_list" in value:
            self._name_list = value["name_list"]
        else:
            self._name_list = None

        if "home_planet" in value:
            self._home_id = value["home_planet"]
        else:
            self._home_id = None

        self.id = self._gen_id()
        
        self.base = None
        self.children = None 
        self.pops = None
        self.leaders = None

        if "base" in value:
            self.base_index = int(value["base"])
        else:
            self.base_index = None

    def _gen_id(self):
        m = hashlib.md5()

        m.update(bytearray(self._class, "utf-8"))
        m.update(bytearray(self._portrait, "utf-8"))

        if self._name_list:
            m.update(bytearray(self._name_list, "utf-8"))

        if self._home_id:
            m.update(bytearray(self._home_id, "utf-8"))

        for trait in self.traits:
            m.update(bytearray(trait, "utf-8"))

        return m.hexdigest()

    def __str__(self):
        return f"Species({self.id},name={self.name})"