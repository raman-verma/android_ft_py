#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import random

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

random.seed(1)


class Model(QtCore.QObject):
    item_added = QtCore.pyqtSignal(int)
    item_removed = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.items = {}

    def add_item(self):
        guid = random.randint(0, 10000)
        new_item = {
            "pos": [random.randint(50, 100), random.randint(50, 100)]
        }
        self.items[guid] = new_item
        self.item_added.emit(guid)

    def remove_item(self):
        list_keys = list(self.items.keys())

        if len(list_keys) == 0:
            self.item_removed.emit(-1)
            return

        guid = random.choice(list_keys)
        self.item_removed.emit(guid)
        del self.items[guid]


class View1():

    def __init__(self, main_window):
        self.main_window = main_window

        view = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene(None)
        self.scene.addText("Hello, world!")

        view.setScene(self.scene)
        view.setStyleSheet("background-color: white;")

        main_window.setCentralWidget(view)


class View2():
    add_item = QtCore.pyqtSignal(int)
    remove_item = QtCore.pyqtSignal(int)

    def __init__(self, main_window):
        self.main_window = main_window

        button_add = QtWidgets.QPushButton("Add")
        button_remove = QtWidgets.QPushButton("Remove")
        vbl = QtWidgets.QVBoxLayout()
        vbl.addWidget(button_add)
        vbl.addWidget(button_remove)
        view = QtWidgets.QWidget()
        view.setLayout(vbl)

        view_dock = QtWidgets.QDockWidget('View2', main_window)
        view_dock.setWidget(view)

        main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, view_dock)

        model = main_window.model
        button_add.clicked.connect(model.add_item)
        button_remove.clicked.connect(model.remove_item)


class Controller():

    def __init__(self, main_window):
        self.main_window = main_window

    def on_item_added(self, guid):
        view1 = self.main_window.view1
        model = self.main_window.model

        print("item guid={0} added".format(guid))
        item = model.items[guid]
        x, y = item["pos"]
        graphics_item = QtWidgets.QGraphicsEllipseItem(x, y, 60, 40)
        item["graphics_item"] = graphics_item
        view1.scene.addItem(graphics_item)

    def on_item_removed(self, guid):
        if guid < 0:
            print("global cache of items is empty")
        else:
            view1 = self.main_window.view1
            model = self.main_window.model

            item = model.items[guid]
            x, y = item["pos"]
            graphics_item = item["graphics_item"]
            view1.scene.removeItem(graphics_item)
            print("item guid={0} removed".format(guid))


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # (M)odel ===> Model/Library containing should be UI agnostic, right now it's not
        self.model = Model()

        # (V)iew      ===> Coupled to UI
        self.view1 = View1(self)
        self.view2 = View2(self)

        # (C)ontroller ==> Coupled to UI
        self.controller = Controller(self)

        self.attach_views_to_model()

    def attach_views_to_model(self):
        self.model.item_added.connect(self.controller.on_item_added)
        self.model.item_removed.connect(self.controller.on_item_removed)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    form = MainWindow()
    form.setMinimumSize(800, 600)
    form.show()
    sys.exit(app.exec_())
