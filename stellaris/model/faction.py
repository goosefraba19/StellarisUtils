from .utils import getitem_or_default

class Faction:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)
        self.type = getitem_or_default(value, "type", None)
        self.support = float(getitem_or_default(value, "support", 0))
        self.happiness = float(getitem_or_default(value, "happiness", 0))



        # relationships

        self.country = None
        self.members = None
        self.leader = None

        self.country_id = value["country"]
        self.member_ids = getitem_or_default(value, "members", [])
        self.leader_id = getitem_or_default(value, "leader", None)

    def __str__(self):
        return f"Faction({self.id},name={self.name})"