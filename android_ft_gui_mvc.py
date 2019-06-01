#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton, QMainWindow)
from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
import subprocess


class Model(QObject):
    ITEM, ITEM2 = range(2)

    def __init__(self, main_window):
        self.main_window = main_window

    # List Model
    def createListModel(self):
        model = QStandardItemModel(0, 1)
        model.setHeaderData(self.ITEM, Qt.Horizontal, "DIRectory")
        return model

    # Add data
    def addItem(self, model, item):
        model.insertRow(0)
        model.setData(model.index(0, self.ITEM), item)

    def adbcommand(self):
        process = subprocess.Popen(["adb shell ls"], shell=True, stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        dir_list = [i for i in format(stdout.decode("utf-8")).split("\n")]
        return dir_list

    def getpath(self):
        path = [str(data.data()) for data in self.main_window.view.dataView.selectedIndexes()]
        return path


class View:
    showdir = pyqtSignal(int)

    def __init__(self, main_window):
        self.main_window = main_window
        model = self.main_window.model

        # Edit Box
        self.search_box = QLineEdit()

        # Push button
        button = QPushButton('see list')
        button.setToolTip('Show List of items')

        # Search and button Layout grouping
        horizontal_groupbox = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(button)
        horizontal_groupbox.setLayout(layout)

        # Tree View
        dataGroupBox = QGroupBox("Android Directory")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        self.dataView.setSortingEnabled(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        dataGroupBox.setLayout(dataLayout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(horizontal_groupbox)
        main_layout.addWidget(dataGroupBox)

        main_window.setLayout(main_layout)

        button.clicked.connect(model.getpath)
        self.dataView.clicked.connect(model.getpath)


class Controller:
    def __init__(self, main_window):
        self.main_window = main_window

        model = self.main_window.model.createListModel()
        self.main_window.view.dataView.setModel(model)
        dir_list = self.main_window.model.adbcommand()
        for i in dir_list:
            self.main_window.model.addItem(model, str(i))

    def showpath(self):
        print("sdfsdfsd")
        self.path = self.main_window.model.getpath

        self.main_window.view.search_box.setText(self.path[0])
        self.main_window.view.search_box.setFocus()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Android File Transfer'
        self.setWindowTitle(self.title)

        # Model for the View
        self.model = Model(self)
        # View for the window
        self.view = View(self)
        # Controller for both model and view
        self.controller = Controller(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setMinimumSize(400, 500)
    main_window.show()
    sys.exit(app.exec_())
