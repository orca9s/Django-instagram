class RelationNotExist(Exception):

    def __init__(self, from_user, to_user, relation_type):
        self.from_user = from_user
        self.to_user = to_user
        self.relation_type = relation_type

    def __str__(self):
        return 'Relation (From: {}, To: {}, Type: {})'.format(
            self.from_user,
            self.to_user,
            self.relation_type,
        )