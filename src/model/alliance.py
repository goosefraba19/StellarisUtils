from .utils import getitem_or_default

class Alliance:
    def __init__(self, id, value):
        self.id = id
        self.name = getitem_or_default(value, "name", None)
        self.start_date = getitem_or_default(value, "start_date", None)



        # relationships

        self.leader = None
        self.members = []
        self.associates = []

        self.leader_id = value["leader"]
        self.member_ids = value["members"]