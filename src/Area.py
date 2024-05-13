from PyQt5.QtWidgets import QScrollArea, QShortcut, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QObject, pyqtSignal


class MyArea(QScrollArea):
    book = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = parent
        self.initUi()
        self.setAlignment(Qt.AlignCenter)
        # self inherit QWidget
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.custom_right_menu)

    def initUi(self):
        self.init_action()

    def init_action(self):
        zoom_minus = QShortcut(QKeySequence("Ctrl+-"), self)
        zoom_minus.activated.connect(self.minus)
        zoom_plus = QShortcut(QKeySequence("Ctrl+="), self)
        zoom_plus.activated.connect(self.plus)

        switch_left_ = QShortcut(QKeySequence("←"), self)
        switch_left_.activated.connect(self.left)

        switch_left = QShortcut(QKeySequence(Qt.Key_Left), self)
        switch_left.activated.connect(self.left)

        switch_right_ = QShortcut(QKeySequence("→"), self)
        switch_right_.activated.connect(self.plus)

        switch_right = QShortcut(QKeySequence(Qt.Key_Right), self)
        switch_right.activated.connect(self.right)

    def sebook(s1):
        book = s1

    # 鼠标左键翻页
    def mousePressEvent(self, event):
        pos = event.pos().x()
        width = self.size().width()
        if event.button() == Qt.LeftButton:
            if pos > width * 2 / 3:
                self.right()
            elif pos < width / 3:
                self.left()

    # 右键菜单
    def custom_right_menu(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("放大图片（Ctrl+-）")
        opt2 = menu.addAction("缩小图片（Ctrl+=）")
        opt3 = menu.addAction("上一页（←）")
        opt4 = menu.addAction("下一页（→）")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == opt1:
            self.plus()
            return
        elif action == opt2:
            self.minus()
            return
        elif action == opt3:
            self.left()
            return
        elif action == opt4:
            self.right()
            return
        else:
            return

    # 放大
    def plus(self):
        self.widget.zoom_book(plus=True)

    # 缩小
    def minus(self):
        self.widget.zoom_book(plus=False)

    # 下一页
    def right(self):
        self.widget.switch_page(right=True)

    # 前一页
    def left(self):
        self.widget.switch_page(right=False)
