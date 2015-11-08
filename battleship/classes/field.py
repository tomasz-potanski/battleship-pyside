class Field:
    """
    Single field on board
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.battleship = None
        self.was_hit = False

    def get_battleship(self):
        """Returns battleship that is on this field if any"""
        return self.battleship

    def has_battleship(self):
        """Tells if battleship is on this field"""
        return False if self.battleship is None else True

    def set_battleship(self, battleship):
        """Sets battleship on this field"""
        self.battleship = battleship

    def get_was_hit(self):
        """Tells whether field was hit or not"""
        return self.was_hit

    def field_hit(self):
        """Field was hit by bullet"""
        self.was_hit = True
        if self.battleship is None:
            return False
        else:
            self.battleship.was_hit()
            return True