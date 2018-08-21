class Faction:
    def __init__(self, id, value):
        self.id = id
        self.name = value["name"]
        self.type = value["type"]

        if "support" in value:
            self.support = float(value["support"])
        else:
            self.support = 0

        if "happiness" in value:
            self.happiness = float(value["happiness"])
        else:
            self.happiness = 0

        self.country = None
        self.members = None
        self.leader = None

        self.country_id = value["country"]

        if "members" in value:
            self.member_ids = value["members"]
        else:
            self.member_ids = []

        if "leader" in value:
            self.leader_id = value["leader"]
        else:
            self.leader_id = None

    def __str__(self):
        return f"Faction({self.id},name={self.name})"