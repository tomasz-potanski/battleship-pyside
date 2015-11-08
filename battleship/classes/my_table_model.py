from PySide.QtGui import QAbstractTableModel
from PySide.QtCore import Signal
from PySide import Qt


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