from battleship.classes.field import Field


class Board:
    """
    Describes (one half of the) board
    """

    def __init__(self, user, length, width):
        self.user = user
        self.length = length
        self.width = width
        self.board = []
        self.fill_with_fields(length, width)
        self.hit_ship_field = 0
        self.hit_ship_fields = []
        self.total_hit = 0

    def get_hit_ship_fields(self):
        """Returns exact coordinates of fields that was hit and contained battleship"""
        return self.hit_ship_fields

    def get_total_hit(self):
        """Returns total amount of shots on this board"""
        return self.total_hit

    def get_hit_ship_field(self):
        """Tells how many field containing ships was hit"""
        return self.hit_ship_field

    def can_fire(self, x, y):
        """
        Tests if user has already hit this field

        :param x: x coordinate
        :param y: y coordinate
        """
        try:
            return not self.board[x][self.get_length() - y - 1].get_was_hit()
        except IndexError:
            return False

    def fire(self, x, y):
        """
        Hits specific field (given by coordinates)

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.can_fire(x, y):
            self.total_hit += 1
            if self.board[x][self.get_length() - y - 1].field_hit():
                self.hit_ship_field += 1
                self.hit_ship_fields.append((x, y))

    def set_user(self, user):
        """Sets that this board belongs to given user"""
        self.user = user

    def get_user(self):
        """Returns user who own this board"""
        return self.user

    def has_ship_on(self, x, y):
        """
        Checks if on this specific field (given by coordinates) is a battleship

        :param x: x coordinate
        :type x: `int`
        :param y: y coordinate
        :type y: `int`
        """
        return self.board[x][self.get_length() - y - 1].has_battleship()

    def get_length(self):
        """Returns board's length"""
        return self.length

    def get_width(self):
        """Returns board's width"""
        return self.width

    def fill_with_fields(self, length, width):
        """
        Called in __init__(), fills baord with fields

        :param length: x dimension
        :type length: `int`
        :param width: y dimension
        :type width: `int`
        """
        for i in range(width):
            self.board.append([])
            for j in range(length):
                self.board[i].append(Field(i, j))

    def can_be_placed(self, x, y, ship, orientation):
        """
        Tests whether specific ship can be placed properly on this board using given coordinates

        :param x: x coordinate
        :type x: `int`
        :param y: y coordinate
        :type y: `int`
        :param ship: ship to place
        :type ship: `Battleship`
        :param orientation: vertical or horizontal
        :type orientation: `string`
        """
        length = ship if type(1) == type(ship) else ship.get_length()
        if orientation == "horizontal":
            if x + length - 1 >= self.get_length():
                return False
            for i in range(length):
                if self.board[x + i][self.get_length() - y - 1].has_battleship():
                    return False
            return True
        elif orientation == "vertical":
            if y - length + 1 < 0:
                return False
            for i in range(length):
                if self.board[x][self.get_length() - y + i - 1].has_battleship():
                    return False
            return True
        else:
            return False

    def place_ship(self, x, y, ship, orientation):
        """
        Places specific ship on this board in a given way

        :param x: x coordinate
        :param y: y coordinate
        :param ship: ship to place
        :param orientation: vertical or horizontal
        :type orientation: `string`
        :return:
        """
        if orientation == "horizontal":
            for i in range(ship.get_length()):
                self.board[x + i][self.get_length() - y - 1].set_battleship(ship)
        elif orientation == "vertical":
            for i in range(ship.get_length()):
                self.board[x][self.get_length() - y + i - 1].set_battleship(ship)
        else:
            raise Exception("unknown orientation type")

    def set_battleship(self, x, y, ship, orientation):
        """
        Places battleship if it is possible

        :param x: x coordinate
        :param y: y coordinate
        :param ship: specific ship
        :param orientation: vertical or horizontal
        :type orientation: `string`
        :return: True if ship can be placed, False otherwise
        """
        if self.can_be_placed(x, y, ship, orientation):
            self.place_ship(x, y, ship, orientation)
            self.user.add_ship(ship)
            return True
        else:
            return False