from battleship.classes.dialog_window import DialogWindow


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