#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Battleship python game with GUI in QT (PySide)

Author: Tomasz Potanski, tomasz@potanski.pl
"""

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtGui
import math
import random
import operator
from time import time


class Timer:
    """
    Timer class to calculate the duration of the game
    """

    def __init__(self):
        self._elapsed = 0.0
        self._starttime = time()
        self._started = False

    def start(self):
        self._starttime = time()
        self._started = True

    def stop(self):
        self._elapsed += (time() - self._starttime)
        self._started = False

    def reset(self):
        self._elapsed = 0.0

    def get_elapsed(self):
        if self._started:
            return self._elapsed + time() - self._starttime
        else:
            return self._elapsed

    def get_result(self):
        # tuple: (hours, minutes, seconds, microseconds)
        if self._started:
            timee = self._elapsed + time() - self._starttime
        else:
            timee = self._elapsed

        seconds = timee
        minutes = seconds // 60
        seconds = round((seconds % 60), 3)
        hours = minutes // 60
        minutes %= 60
        mseconds = round((timee * 100), 3)
        return hours, minutes, seconds, mseconds


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
        Tests whether specific ship can be placed properly on this board using
        given coordinates

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


class GameWindow(QWidget):
    """
    Widget containing GameBoard and a few controls (like reset button)
    """

    def __init__(self, game):
        super(GameWindow, self).__init__()
        self.game = game
        self.status_text = """Place your ships
right click - rotate
left click - place"""
        self.status_label = None

        self.init_gui()

    def set_status_text(self, text):
        """Sets text with information for players"""
        self.status_text = text
        self.status_label.setText(text)
        self.status_label.update()

    def init_gui(self):
        """Initializes user interface"""
        self.status_label = QLabel(self.status_text)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.status_label)
        hbox.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.game)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(1)
        again_button = QPushButton("Reset")
        again_button.clicked.connect(self.reset)
        hbox2.addWidget(again_button)
        hbox2.addStretch(1)

        vbox.addLayout(hbox2)

        self.setLayout(vbox)
        self.setWindowTitle("Battleship game")
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setFixedSize(self.sizeHint())
        self.resize(self.sizeHint())

    def reset(self):
        """Play once again with new settings"""

        self.dialogWindow = DialogWindow()
        self.dialogWindow.show()
        self.close()


class MyTableModel(QAbstractTableModel):
    """
    Custom table model for presenting amount of ships for user
    """

    def __init__(self, parent, my_list, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.my_list = my_list
        self.header = header

    def rowCount(self, parent):
        return len(self.my_list)

    def columnCount(self, parent):
        return len(self.my_list[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.my_list[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.my_list = sorted(self.my_list,
                              key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.my_list.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class EndScores(QWidget):
    """
    Widget presenting scores at the end of the game
    """

    def __init__(self, s_u1, s_u2):
        super(EndScores, self).__init__()
        self.s_u1 = s_u1
        self.s_u2 = s_u2
        self.d = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize User Interface
        """
        winner_text = \
            "You are the winner! Congrats!" if self.s_u1 > self.s_u2 else "Your opponent is the winner"

        points_u1_text = "Your points: %d" % self.s_u1
        points_u2_text = "Your opponent's points: %d" % self.s_u2

        winner_label = QtGui.QLabel(winner_text)
        winner_hbox = QtGui.QHBoxLayout()
        winner_hbox.addStretch(1)
        winner_hbox.addWidget(winner_label)
        winner_hbox.addStretch(1)

        your_points_label = QtGui.QLabel(points_u1_text)
        your_points_hbox = QtGui.QHBoxLayout()
        your_points_hbox.addStretch(1)
        your_points_hbox.addWidget(your_points_label)
        your_points_hbox.addStretch(1)

        opponent_points_label = QtGui.QLabel(points_u2_text)
        opponent_points_hbox = QtGui.QHBoxLayout()
        opponent_points_hbox.addStretch(1)
        opponent_points_hbox.addWidget(opponent_points_label)
        opponent_points_hbox.addStretch(1)

        controls = QtGui.QHBoxLayout()
        restart = QPushButton("Restart")
        restart.clicked.connect(self.restartt)
        close = QPushButton("Close")
        close.clicked.connect(self.close_custom)
        controls.addWidget(restart)
        controls.addWidget(close)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(winner_hbox)
        vbox.addLayout(your_points_hbox)
        vbox.addLayout(opponent_points_hbox)
        vbox.addLayout(controls)

        self.setLayout(vbox)

        self.setWindowTitle("Game over!")

    def close_custom(self):
        """
        Performs after close button is pressed
        """
        self.close()

    def restartt(self):
        """
        Performs after reset button is pressed
        """
        self.d = DialogWindow()
        self.d.show()
        self.close()


class DialogWindow(QWidget):
    """
    Initial window that collect necessary data from the user
    """

    def __init__(self):
        super(DialogWindow, self).__init__()
        self.combo = QtGui.QComboBox()
        self.length_input = QDoubleSpinBox()
        self.width_input = QDoubleSpinBox()
        self.ships_l = [(5, 1), (4, 1), (3, 1)]
        self.ships_d = {5: 1, 4: 1, 3: 1}
        self.u1 = None
        self.u2 = None
        self.b1 = None
        self.b2 = None
        self.g = None
        self.gw = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface
        """
        label = QtGui.QLabel("Choose game type:")
        computer = QtGui.QPushButton("Play with computer")
        computer.clicked.connect(self.play_with_computer)

        label_level = QtGui.QLabel("Choose difficulty level")

        comp_hbox = QtGui.QHBoxLayout()
        comp_hbox.addWidget(computer)
        comp_hbox.addWidget(label_level)
        self.combo.addItem("Very easy")
        self.combo.addItem("Medium")
        self.combo.addItem("Nightmare!")
        comp_hbox.addWidget(self.combo)

        network = QtGui.QPushButton("Play with human over network")
        network.setEnabled(False)
        image = QImage()
        image.load("./resources/image.jpg")
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image))
        image_label.setFixedSize(QSize(640, 360))

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(label)
        hbox.addStretch(1)

        h_conf_length = QtGui.QHBoxLayout()
        length_label = QLabel("Set board length: ")
        h_conf_length.addWidget(length_label)
        self.length_input.setMaximum(5)
        self.length_input.setMinimum(5)
        self.length_input.setDecimals(0)
        h_conf_length.addWidget(self.length_input)

        width_label = QLabel("Set board width: ")
        h_conf_length.addWidget(width_label)
        self.width_input.setMaximum(5)
        self.width_input.setMinimum(5)
        self.width_input.setDecimals(0)
        h_conf_length.addWidget(self.width_input)

        header = ['Ship length', 'Amount of ships']
        table_model = MyTableModel(self, self.ships_l, header)
        table_view = QTableView()
        table_view.setModel(table_model)
        table_view.resizeColumnsToContents()
        table_view.setSortingEnabled(True)
        table_view.setColumnWidth(0, table_view.width() / 2 - 5)
        table_view.setColumnWidth(1, table_view.width() / 2 - 5)
        table_view.setFixedHeight(200)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(image_label)
        vbox.addLayout(hbox)
        vbox.addLayout(comp_hbox)
        vbox.addWidget(network)
        vbox.addLayout(h_conf_length)
        vbox.addWidget(table_view)

        self.setLayout(vbox)

        self.setWindowTitle("Choose gametype")
        self.setFixedSize(self.minimumSize())
        self.resize(self.minimumSize())

    def play_with_computer(self):
        """
        Performs after "play with computer" button is pressed,
        sets up necessary settings
        :return:
        """
        self.u1 = User(1, "local")
        self.u2 = User(2, "computer", self.combo.currentText())
        self.b1 = Board(self.u1, int(self.length_input.value()), int(self.width_input.value()))
        self.b2 = Board(self.u2, int(self.length_input.value()), int(self.width_input.value()))
        self.g = GameBoard(self.b1, self.b2, self.ships_l, self)

        self.gw = GameWindow(self.g)
        self.g.set_game_window(self.gw)
        self.gw.show()
        self.close()

    def center(self):
        """
        Should center the widget on the screen
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)

dialog = DialogWindow()
dialog.show()

app.exec_()



