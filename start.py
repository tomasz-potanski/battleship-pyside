#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Battleship python game with GUI in QT (PySide)

Author: Tomasz Potanski, tomasz@potanski.pl
"""

from PySide.QtGui import QApplication

from battleship.classes import DialogWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dialog = DialogWindow()
    dialog.show()

    app.exec_()