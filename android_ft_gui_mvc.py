#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from functools import partial
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton, QMainWindow, QAbstractItemView)
from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
import subprocess


class Model(QObject):
    ITEM, ITEM2 = range(2)

    def __init__(self, main_window):
        self.main_window = main_window
        self.path = ""

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
        return self.path

    def setpath(self, path):
        self.path = path + "/"


class View(QWidget):
    showdir_signal = pyqtSignal()
    openfolder_signal = pyqtSignal()

    def __init__(self, main_window):
        super(View, self).__init__()
        self.main_window = main_window

        # Initial Layout
        # Edit Box
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(partial(setattr, self, "folderpath"))

        # Push button
        open_folder_button = QPushButton('see list')
        open_folder_button.setToolTip('Show List of items')

        # Search and button Layout grouping
        horizontal_groupbox = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(open_folder_button)
        horizontal_groupbox.setLayout(layout)

        # Central Layout for data view
        # Tree View
        data_groupBox = QGroupBox("Android Directory")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        self.dataView.setSortingEnabled(True)
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.dataView)
        data_groupBox.setLayout(data_layout)

        # Footer Layout
        labelpath = QLabel("PATH:")
        self.path_label = QLabel()
        push_button = QPushButton("Push")
        push_button.setToolTip("Push this path to desire folder")

        footer_groupbox = QGroupBox()
        footer_layout = QHBoxLayout()
        footer_layout.addWidget(labelpath)
        footer_layout.addWidget(self.path_label)
        footer_layout.addWidget(push_button, alignment=Qt.AlignCenter)
        footer_groupbox.setLayout(footer_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(horizontal_groupbox)
        main_layout.addWidget(data_groupBox)
        main_layout.addWidget(footer_groupbox)

        main_window.setLayout(main_layout)

        open_folder_button.clicked.connect(self.openfolder_signal)
        self.dataView.doubleClicked.connect(self.showdir_signal)


class Controller:
    def __init__(self, main_window):
        self._main_window = main_window
        self._model = self._main_window.model
        self._view = self._main_window.view

        model = self._model.createListModel()
        self._main_window.view.dataView.setModel(model)
        dir_list = self._model.adbcommand()
        for i in dir_list:
            self._model.addItem(model, str(i))

        self._view.showdir_signal.connect(self.showfoldername)
        self._view.openfolder_signal.connect(self.showopenfolder)

    def showfoldername(self):
        folder_name = [str(data.data()) for data in self._view.dataView.selectedIndexes()]
        self._view.search_box.setText(str(folder_name[0]))
        self._view.search_box.setFocus()

    def showopenfolder(self):
        self._model.path = self._view.folderpath
        self._model.setpath(self._model.path)

        self._view.path_label.setText(self._model.getpath())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Android File Transfer'
        self.setWindowTitle(self.title)

        # Model for the View
        # A model is the entity that keeps the information.
        self.model = Model(self)

        # Views for the window.
        # The view is the entity that shows the information.
        self.view = View(self)

        # Controller for both model and view.
        # The controller is the one that controls the flow of sight data according to a certain logic.
        self.controller = Controller(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setMinimumSize(400, 500)
    main_window.show()
    sys.exit(app.exec_())
