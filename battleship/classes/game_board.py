from battleship.classes.battleship import BattleShip
from battleship.classes.end_scores import EndScores
EndScores

class GameBoard(QtGui.QWidget):
    """
    Widget on which game board is being drawn
    """

    def __init__(self, board1, board2, list_of_ships, dialog_window, parent=None):
        super(GameBoard, self).__init__()

        self.parent = parent
        assert (board1.get_length() == board2.get_length())
        assert (board1.get_width() == board2.get_width())

        self.b1 = board1
        self.b2 = board2
        self.dialog_window = dialog_window
        self.ships_original = list_of_ships.copy()
        self.ships_to_place_u1 = list_of_ships.copy()
        self.ships_to_place_u2 = list_of_ships.copy()
        self.placement = True
        self.placement_vertical_orientation = True
        self.last_board_x_square = -1
        self.last_board_y_square = -1
        self.last_board = -1

        self.real_game = False
        self.user_turn = True
        self.game_over = False
        self.es = None
        self.game_window = None

        self.can_place_ship = False

        self.resize(250, 520)
        self.setWindowTitle("Battleship game")
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setMouseTracking(True)

    def set_game_window(self, game_window):
        """Sets reference to game window, it is necessary further"""
        self.game_window = game_window

    def get_game_window(self):
        """Returns reference to game window"""
        return self.game_window

    def _coordinates_from_position(self, x, y):
        """
        Useful function that transforms mouse x and y position
        into specific square coordinates

        :param x: mouse x position
        :param y: mouse y position
        """
        # assuming square size is 50px x 50px
        if y > 50 * self.b2.get_length() + 20:
            board = 1
            ry = math.floor((y - 50 * self.b2.get_length() - 20) / 50)
        else:
            board = 2
            ry = math.floor(y / 50)

        return math.floor(x / 50), ry, board

    def square_pos_changed(self):
        """
        Function fires if mouse hovers different square than previously
        """
        self.update()

    def mouseMoveEvent(self, event):
        act_x, act_y, act_board = self._coordinates_from_position(event.x(), event.y())
        if act_x != self.last_board_x_square or act_y != self.last_board_y_square \
                or act_board != self.last_board:
            if act_x != self.b1.get_width() and act_y != self.b1.get_length():
                self.last_board_x_square = act_x
                self.last_board_y_square = act_y
                self.last_board = act_board
                self.square_pos_changed()

    def mouseReleaseEvent(self, event):
        if self.placement:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.can_place_ship:
                    s_desc = self.ships_to_place_u1.pop(0)
                    s = BattleShip(s_desc[0], self.b1.get_user())
                    self.b1.set_battleship(self.last_board_x_square, self.last_board_y_square,
                                           s, "vertical" if self.placement_vertical_orientation else "horizontal")
                    if s_desc[1] > 1:
                        self.ships_to_place_u1.push((s_desc[0], s_desc[1] - 1))
                        self.ships_to_place_u1.sort(reversed=True)
                    if len(self.ships_to_place_u1) == 0:
                        self.can_place_ship = False
                        self.placement = False
                        self.ai_place_ships()
            elif event.button() == Qt.MouseButton.RightButton:
                self.placement_vertical_orientation = not self.placement_vertical_orientation
            else:
                raise Exception("unknown button")
        elif self.real_game and self.user_turn and self.last_board == 2 \
                and self.b2.can_fire(self.last_board_x_square, self.last_board_y_square):
            self.b2.fire(self.last_board_x_square, self.last_board_y_square)
            self.game_over = self.check_if_end()
            self.user_turn = False
            self.ai_turn()
        else:
            # it's not your turn
            pass

    def nightmare_select_field(self):
        """
        Field selection algorithm for the most difficult AI

        :return: (x, y) of selected field
        """
        for x in range(self.b1.get_width()):
            for y in range(self.b1.get_length()):
                if self.b1.has_ship_on(x, y) and self.b1.can_fire(x, y):
                    return x, y

    def medium_select_field(self):
        """
        Field selection algorithm for middle difficulty AI

        :return: (x, y) of selected field
        """
        arrows = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for field in self.b1.get_hit_ship_fields():
            for arrow in arrows:
                if (0 <= field[0] + arrow[0]) and (field[0] + arrow[0] < self.b1.get_width()):
                    if (0 <= field[1] + arrow[1]) and (field[1] + arrow[1] < self.b1.get_length()):
                        if self.b1.can_fire(field[0] + arrow[0], field[1] + arrow[1]):
                            return field[0] + arrow[0], field[1] + arrow[1]
        return self.easy_select_field()

    def easy_select_field(self):
        """
        Field selection algorithm for the least difficult AI

        :return: (x, y) of selected field
        """
        while True:
            x = random.randint(0, self.b1.get_width() - 1)
            y = random.randint(0, self.b1.get_length() - 1)
            if self.b1.can_fire(x, y):
                return x, y

    def ai_turn(self):
        """
        AI selects field and fire to it

        :return:
        """
        if self.b2.get_user().get_level() == 3:
            # Nightmare!
            (x, y) = self.nightmare_select_field()
        elif self.b2.get_user().get_level() == 2:
            (x, y) = self.medium_select_field()
        else:
            (x, y) = self.easy_select_field()

        self.b1.fire(x, y)
        self.update()
        self.game_over = self.check_if_end()
        self.user_turn = True

    def check_if_end(self):
        """
        Check if game is over ;)

        :return:
        """
        self.update()
        if self.b1.get_user().get_amount_of_ships() == 0 or self.b2.get_user().get_amount_of_ships() == 0:
            (s_u1, s_u2) = self.calculate_scores()
            self.game_over = True
            self.show_scores(s_u1, s_u2)
            return True
        return False

    def show_scores(self, s_u1, s_u2):
        """
        Shows Widget to present scores at the end of the game

        :param s_u1: User 1 points
        :param s_u2: User 2 points
        :return:
        """
        self.es = EndScores(s_u1, s_u2)
        self.es.show()
        self.game_window.close()

    def calculate_scores(self):
        """
        Function calculates points at the end of the game

        :return (u1 points, u2 points)
        """
        points_u1 = 0
        points_u2 = 0
        if self.game_over:
            maximum_ship_fields = 0
            ships_amount = 0
            for leng, amount in self.ships_original:
                maximum_ship_fields += leng * amount
                ships_amount += amount

            # points for victory (300 - 0)
            if self.b1.get_user().get_amount_of_ships() == 0:
                points_u2 += 300
            else:
                points_u1 += 300

            # points for destroyed ships (20 per ship)
            points_u1 += 20 * (ships_amount - self.b2.get_user().get_amount_of_ships())
            points_u2 += 20 * (ships_amount - self.b1.get_user().get_amount_of_ships())

            # points for accuracy (ratio * 150)
            ratio_u1 = self.b2.get_hit_ship_field() / self.b2.get_total_hit()
            ratio_u2 = self.b1.get_hit_ship_field() / self.b1.get_total_hit()
            points_u1 += ratio_u1 * 150
            points_u2 += ratio_u2 * 150

        return points_u1, points_u2

    def ai_place_ships(self):
        """
        AI places ships on board
        """
        successfully_placed = False
        ships_to_place = self.ships_to_place_u2.copy()
        j = 0
        while (not successfully_placed) and (j < 20):
            length = ships_to_place[0][0]
            ship_successfully_placed = False
            i = 0
            ship_to_place = BattleShip(length, self.b2.get_user())
            while (not ship_successfully_placed) and (i < 50):
                x = random.randint(0, self.b2.get_width() - 1)
                y = random.randint(0, self.b2.get_length() - 1)
                orientation = random.randint(0, 1)
                ship_successfully_placed = self.b2.set_battleship(x, y, ship_to_place,
                                                                  "vertical" if orientation == 1 else 0)
                i += 1
            if ship_successfully_placed:
                sh = ships_to_place.pop(0)
                if sh[1] > 1:
                    ships_to_place.append((sh[0], sh[1] - 1))
                    ships_to_place.sort(reversed=True)
                if len(ships_to_place) == 0:
                    successfully_placed = True
            else:
                ships_to_place = self.ships_to_place_u2.copy()
        if successfully_placed:
            self.real_game = True
            self.user_turn = True
            self.game_window.set_status_text("""Choose field on enemy's board and fire!""")
        else:
            # placing 'em manually
            ships_to_place = self.ships_to_place_u2.copy()
            y = self.b2.get_length() - 1
            x = -1
            success = True
            for (leng, _) in ships_to_place:
                x += 1
                if ship_to_place is not None:
                    success &= self.b2.set_battleship(x, y, ship_to_place, "vertical")
            if success:
                self.real_game = True
                self.user_turn = True
                self.game_window.setStatusText("""Choose field on enemy's board and fire!""")
            else:
                raise Exception("Cannot place ships")

    def size(self):
        return QSize(250, 520)

    def sizeHint(self):
        return QSize(250, 520)

    def paintEvent(self, event):
        """
        Does the painting
        """
        painter = QPainter()
        painter.begin(self)

        bottom_border = 50 * self.b1.get_length() + 20 + 50 * self.b2.get_length()
        right_border = 50 * self.b1.get_width()
        water_brush = QBrush(Qt.blue)
        ship_brush = QBrush(Qt.black)
        red_brush = QBrush(Qt.red)
        division_brush = QBrush(Qt.darkGray)
        for i in range(self.b1.get_width()):
            for j in range(self.b1.get_length()):
                if self.b1.has_ship_on(i, j):
                    brush = ship_brush
                else:
                    brush = water_brush
                painter.fillRect(QRect(50 * i, bottom_border - 50 * (self.b1.get_length() - j), 50, 50), brush)
                if not self.b1.can_fire(i, j):
                    painter.fillRect(QRect(50 * i + 10, bottom_border - 50 * (self.b1.get_length() - j) + 10, 30, 30),
                                     red_brush)
                painter.drawLine(0, bottom_border - 50 * (self.b1.get_length() - j), right_border, bottom_border - 50
                                 * (self.b1.get_length() - j))
            painter.drawLine(i * 50, bottom_border, i * 50, 0)

        painter.fillRect(QRect(0, 50 * self.b1.get_length(), 50 * self.b1.get_width(), 20),
                         division_brush)

        bottom_border_b2 = 50 * self.b2.get_length()
        for i in range(self.b2.get_width()):
            for j in range(self.b2.get_length()):
                if self.b2.has_ship_on(i, j):
                    brush = ship_brush
                    if not self.b2.can_fire(i, j):
                        painter.fillRect(QRect(50 * i, bottom_border_b2 - 50 * (self.b2.get_length() - j), 50, 50),
                                         brush)
                    else:
                        painter.fillRect(QRect(50 * i, bottom_border_b2 - 50 * (self.b2.get_length() - j), 50, 50),
                                         water_brush)
                else:
                    brush = water_brush
                    painter.fillRect(QRect(50 * i, bottom_border_b2 - 50 * (self.b2.get_length() - j), 50, 50), brush)
                if not self.b2.can_fire(i, j):
                    painter.fillRect(QRect(50 * i + 10, bottom_border_b2 - 50 * (self.b2.get_length() - j) + 10, 30,
                                           30),
                                     red_brush)
                painter.drawLine(0, bottom_border_b2 - 50 * (self.b2.get_length() - j), right_border, bottom_border_b2
                                 - 50 * (self.b2.get_length() - j))
            painter.drawLine(i * 50, bottom_border_b2, i * 50, 0)

        if len(self.ships_to_place_u1) > 0 and (self.last_board_y_square != -1 or self.last_board_x_square != -1) \
                and self.last_board == 1:
            # draw imaginary ship placement
            length = self.ships_to_place_u1[0][0]
            ok_brush = QBrush(Qt.green)
            incorrect_brush = QBrush(Qt.red)
            fields_to_color = []

            if self.b1.can_be_placed(self.last_board_x_square, self.last_board_y_square,
                                     length, "vertical" if self.placement_vertical_orientation else "horizontal"):
                brush = ok_brush
                self.can_place_ship = True
            else:
                brush = incorrect_brush
                self.can_place_ship = False
            for i in range(length):
                if self.placement_vertical_orientation:
                    if self.last_board_y_square - i >= 0:
                        fields_to_color.append((self.last_board_x_square, self.last_board_y_square - i))
                else:
                    if self.last_board_x_square + i < self.b1.get_width():
                        fields_to_color.append((self.last_board_x_square + i, self.last_board_y_square))

            for field in fields_to_color:
                (x, y) = self.square_coordinates_to_position(field[0], field[1],
                                                             self.last_board)
                painter.fillRect(QRect(x, y, 50, 50), brush)
        if self.real_game and self.user_turn and self.last_board == 2:
            (x, y) = self.square_coordinates_to_position(self.last_board_x_square, self.last_board_y_square,
                                                         self.last_board)
            brush = QBrush(Qt.red)
            painter.fillRect(QRect(x, y, 50, 50), brush)

        painter.end()

    def square_coordinates_to_position(self, mx, my, board):
        """
        Calculates the bottom square of specific rectangle
        over that mouse is currently located

        :param mx: square x coordinate
        :param my: square y coordinate
        :param board: board number
        :return: (x, y) - position of left bottom corner of this square
        """
        x = mx * 50
        if my >= self.b2.get_length():
            my -= 1
        y = my * 50
        if board == 1:
            y += self.b2.get_length() * 50 + 20
        return x, y