#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from functools import partial
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QPushButton, QMainWindow, QAbstractItemView)
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import subprocess
import re


class Model(QObject):
    ITEM, ITEM2 = range(2)

    def __init__(self, main_window):
        super().__init__()
        self.adb = 'adb'
        self._main_window = main_window
        self.full_path = ""
        self.initial_dir = "sdcard/"
        self.destination_folder = '/Users/ramanverma/Desktop/m_device/'
        self.list_of_path = []

    # List Model
    def createListModel(self):
        model = QStandardItemModel(0, 1)
        model.setHeaderData(self.ITEM, Qt.Horizontal, "DIRectory")
        return model

    # Add data
    def addItem(self, model, item):
        model.insertRow(0)
        model.setData(model.index(0, self.ITEM), item)

    def device_list_parsed(self, *args):
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        print(args)
        stdout = process.communicate()[0]
        dir_list = [i.replace(" ", "\\ ") for i in format(stdout.decode("utf-8")).split("\n")]

        # Send the list of files to Model.
        model = self.createListModel()
        self._main_window.view.dataView.setModel(model)
        for i in sorted(dir_list, reverse=True):
            self.addItem(model, str(i))

    def _adb(self, *args):
        return self.device_list_parsed(self.adb, *args)

    def adb_shell(self, *args):
        return self._adb('shell', *args)

    def adb_shell_ls(self, *args):
        return self.adb_shell('ls', *args)

    def add_path_in_list(self, path):
        self.list_of_path.append(path)
        self.set_path()

    def remove_path_in_list(self):
        self.list_of_path.pop()
        self.set_path()

    def get_path(self):
        return self.full_path

    def set_path(self):
        seprator = '/'
        self.full_path = self.initial_dir + seprator.join(self.list_of_path)


class View(QWidget):
    single_click_event = pyqtSignal()
    double_click_event = pyqtSignal()
    go_back_signal = pyqtSignal()
    pull_file_signal = pyqtSignal()

    def __init__(self, main_window):
        super(View, self).__init__()
        self.main_window = main_window

        label_path1 = QLabel("Copy till here: ")

        # Initial Layout
        # Edit Box
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(partial(setattr, self, "folderpath"))

        # Push button
        go_back_button = QPushButton('Back')
        go_back_button.setToolTip('Show List of items')

        # Search and button Layout grouping
        horizontal_groupbox = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(label_path1)
        layout.addWidget(self.search_box)
        layout.addWidget(go_back_button)
        horizontal_groupbox.setLayout(layout)

        # Central Layout for data view
        # Tree View
        data_groupBox = QGroupBox("Android Directory")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        # self.dataView.setSortingEnabled(True)
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.dataView)
        data_groupBox.setLayout(data_layout)

        # Footer Layout
        label_path2 = QLabel("PATH:")
        label_path2.setStyleSheet("border: .5px solid black; max-width:50px;")
        self.path_label_name = QLabel()
        self.path_label_name.setStyleSheet("border: 1px solid black; min-width:450px;")
        self.path_label_name.setWordWrap(True)
        pull_button = QPushButton("Pull")
        pull_button.setToolTip("Push this path to desire folder")
        pull_button.setStyleSheet("min-width: 70px;min-height:15px")

        footer_groupbox = QGroupBox()
        footer_layout = QHBoxLayout()
        footer_layout.addWidget(label_path2)
        footer_layout.addWidget(self.path_label_name)
        footer_layout.addWidget(pull_button, alignment=Qt.AlignCenter)
        footer_groupbox.setLayout(footer_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(horizontal_groupbox)
        main_layout.addWidget(data_groupBox)
        main_layout.addWidget(footer_groupbox)

        main_window.setLayout(main_layout)

        # Signals to button for do event and then show in view
        go_back_button.clicked.connect(self.go_back_signal)
        self.dataView.clicked.connect(self.single_click_event)
        self.dataView.doubleClicked.connect(self.double_click_event)
        pull_button.clicked.connect(self.pull_file_signal)


class Controller:
    def __init__(self, main_window):
        self._main_window = main_window
        self._model = self._main_window.model
        self._view = self._main_window.view
        self.folder_name = ''
        self._model.adb_shell('ls ' + self._model.initial_dir)  # show list of initial directory.

        self._view.single_click_event.connect(self.show_item_name)
        self._view.double_click_event.connect(self.show_folder_list_items)
        self._view.go_back_signal.connect(self.go_back_fun)
        self._view.pull_file_signal.connect(self.pull_this_file)

    def show_item_name(self):
        self.folder_name = [str(data.data()) for data in self._view.dataView.selectedIndexes()]
        self._view.search_box.setText(str(self.folder_name[0]))
        # self._view.search_box.setFocus()

    def show_folder_list_items(self):
        reg = r"\.\w+"

        if self._view.dataView.selectedIndexes()[0].row() == 0:
            try:
                self._model.remove_path_in_list()
                self._model.adb_shell_ls(self._model.get_path())
                self._view.path_label_name.setText(self._model.get_path())
            except IndexError:
                pass
        else:
            if not re.search(reg, str(self.folder_name[0])):    #not working properly, as folder containing '.' is not fine

                # Giving selected item to path list.
                self._model.add_path_in_list(str(self.folder_name[0]))  # add selected folder in the list.
                self._view.path_label_name.setText(self._model.get_path())  # set the total path in below label
                self._model.adb_shell_ls(self._model.get_path())  # run command to open the selected folder

    def go_back_fun(self):
        try:
            self._model.remove_path_in_list()
            self._model.adb_shell_ls(self._model.get_path())
            self._view.path_label_name.setText(self._model.get_path())
        except IndexError:
            pass

    def pull_this_file(self):
        if self._model.get_path() is None:
            pass
        else:
            path_to_pull = str(
                "adb pull " + self._model.get_path() + "/" + self._view.search_box.text() + " " + self._model.destination_folder)
            subprocess.Popen(path_to_pull, shell=True, stdout=subprocess.PIPE)
            print("pass")


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
    main_window.setMinimumSize(700, 600)
    main_window.show()
    sys.exit(app.exec_())
