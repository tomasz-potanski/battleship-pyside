class User:
    """
    User class
    """

    def __init__(self, nr, typee, level=1):
        self.nr = nr
        self.type = typee
        self.ships = []
        self.level = 1
        if level == "Medium":
            self.level = 2
        elif level == "Nightmare!":
            self.level = 3

    def get_type(self):
        """Returns type of user e.g., local, computer"""
        return self.type

    def get_level(self):
        """Returns difficulty level if any, e.g., vary easy, medium, nightmare! ;)"""
        return self.level

    def get_ships(self):
        """Returns all understroyed ships of this user"""
        return self.ships

    def get_amount_of_ships(self):
        """Returns amount of all undersroyed ships of this user"""
        return len(self.ships)

    def remove_ship(self, ship):
        """Removes specific ship form collection"""
        self.ships.remove(ship)

    def add_ship(self, ship):
        """Adds ship to collection"""
        self.ships.append(ship)