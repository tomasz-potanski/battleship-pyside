class BattleShip:
    """
    Class describing Battleship
    """

    def __init__(self, length, user):
        self.length = length
        self.fields_destroyed = 0
        self.belongs_to_user = user

    def was_hit(self):
        """
        Tells that battleship was hit (and is on fire :))
        """
        self.fields_destroyed += 1
        if self.fields_destroyed == self.length:
            self.ship_was_destroyed()

    def ship_was_destroyed(self):
        """
        Tells that ship has been destroyed
        """
        self.belongs_to_user.remove_ship(self)

    def get_length(self):
        """Returns the length of this ship"""
        return self.length

    def __str__(self):
        return "%s - %d" % (self.belongs_to_user.get_type(), self.length)

    def __unicode__(self):
        return "%s - %d" % (self.belongs_to_user.get_type(), self.length)

    def __repr__(self):
        """For printling lists of Battleships"""
        return str(self)