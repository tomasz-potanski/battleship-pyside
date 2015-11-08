from battleship.classes.user import User
from battleship.classes.board import Board
from battleship.classes.game_board import GameBoard
from battleship.classes.game_window import GameWindow


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
        length_label = QtGui.QLabel("Set board length: ")
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
        Performs after "play with computer" button is pressed, sets up necessary settings

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