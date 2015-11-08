from battleship.classes.dialog_window import DialogWindow


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