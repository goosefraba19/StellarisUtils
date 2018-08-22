import hashlib

from .utils import getitem_or_default

class Species:
    def __init__(self, value):
        self.name = value["name"]
        self.traits = getitem_or_default(value["traits"], "trait", [])

        self._class = value["class"]
        self._portrait = value["portrait"]
        self._name_list = getitem_or_default(value, "name_list", None)
        self._home_id = getitem_or_default(value, "home_planet", None)
        self.id = self._gen_id()



        # relationships
        
        self.base = None
        self.children = [] 
        self.pops = []
        self.leaders = []

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