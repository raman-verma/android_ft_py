# from PyQt5.QtWidgets import QApplication, QLabel
#
#
# def label(lists):
#     app = QApplication([])
#     label = QLabel(lists)
#     label.show()
#     app.exec_()


import sys
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Android File Transfer'
        self.left = 20
        self.top = 30
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.model = QFileSystemModel()
        self.model.setRootPath('/Volumes/RV/')
        self.tree = QTreeView()
        self.tree.clicked.connect(self.onClicked)
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

    def onClicked(self, index):
        path = self.sender().model().filePath(index)
        print(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
