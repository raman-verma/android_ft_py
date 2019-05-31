#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt, pyqtSlot,
                          QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton)


class App(QWidget):
    ITEM, ITEM2 = range(2)

    def __init__(self):
        super(App, self).__init__()
        self.title = 'Example GUI'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        # Edit Box
        self.textbox = QLineEdit(self)

        # Push button
        self.button = QPushButton('see list', self)
        self.button.setToolTip('Show List of items')
        self.button.clicked.connect(self.on_click)

        # Search and button Layout grouping
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        self.horizontalGroupBox.setLayout(layout)

        # Tree View
        self.dataGroupBox = QGroupBox("Android Directory")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        # self.dataView.setDisabled(True)
        self.dataView.clicked.connect(self.on_click)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

        # Example for Set the model
        process = subprocess.Popen(["adb shell ls"], shell=True, stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        dirList = [i for i in format(stdout.decode("utf-8")).split("\n")]

        model = self.createListModel(self)
        self.dataView.setModel(model)
        for i in dirList:
            self.addItem(model, str(i))

        self.show()

    # Model
    def createListModel(self, parent):
        model = QStandardItemModel(0, 1, parent)
        model.setHeaderData(self.ITEM, Qt.Horizontal, "DIRectory")
        return model

    # Add data
    def addItem(self, model, item):
        model.insertRow(0)
        model.setData(model.index(0, self.ITEM), item)

    @pyqtSlot()
    def on_click(self):
        path = [str(data.data()) for data in self.dataView.selectedIndexes()]
        self.textbox.setText(path[0])
        self.textbox.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    explorer = App()
    sys.exit(app.exec_())
