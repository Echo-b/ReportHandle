import sys
import os
import json
from PyQt5.QtCore import Qt, QEvent, QRect, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileSystemModel,
    QWidget,
    QVBoxLayout,
    QDesktopWidget,
    QLabel,
    QCheckBox,
    QStyledItemDelegate,
    QStyle,
    QStyleOptionButton,
)
from PyQt5.QtGui import QImage, QPixmap
from Ui_MainWindow import Ui_MainWindow
from handle import Handle
from Area import MyArea
from utils import Size, Point

try:
    import fitz
except ImportError:
    print("请安装 fitz")

# class CheckBoxDelegate(QStyledItemDelegate):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.doubleClickTimer = QTimer()
#         self.doubleClickTimer.setSingleShot(True)
#         self.doubleClickTimer.timeout.connect(self.handleSingleClick)

#     def paint(self, painter, option, index):
#         super().paint(painter, option, index)
#         if index.column() == 0:
#             checked = index.data(Qt.CheckStateRole) == Qt.Checked
#             checkbox_style_option = QStyleOptionButton()
#             checkbox_style_option.state = QStyle.State_Enabled | (
#                 QStyle.State_On if checked else QStyle.State_Off
#             )
#             checkbox_style_option.rect = self.checkboxRect(option)
#             QApplication.style().drawControl(
#                 QStyle.CE_CheckBox, checkbox_style_option, painter
#             )

#     def editorEvent(self, event, model, option, index):
#         if event.type() == QEvent.MouseButtonDblClick:
#             self.doubleClickTimer.stop()
#             self.handleDoubleClick(event, model, index)
#         elif event.type() == QEvent.MouseButtonPress:
#             self.doubleClickTimer.start(QApplication.doubleClickInterval())
#         return super().editorEvent(event, model, option, index)

#     def handleDoubleClick(self, event, model, index):
#         if index.column() == 0:
#             state = model.data(index, Qt.CheckStateRole)
#             model.setData(
#                 index,
#                 Qt.Unchecked if state == Qt.Checked else Qt.Checked,
#                 Qt.CheckStateRole,
#             )

#     def handleSingleClick(self):
#         self.doubleClickTimer.stop()

#     def editorEvent(self, event, model, option, index):
#         # 在用户点击时更改复选框状态
#         if (
#             event.type() == QEvent.MouseButtonRelease
#             and event.button() == Qt.LeftButton
#         ):
#             if self.checkboxRect(option).contains(event.pos()):
#                 checked = model.data(index, Qt.CheckStateRole) == Qt.Checked
#                 model.setData(
#                     index, Qt.Unchecked if checked else Qt.Checked, Qt.CheckStateRole
#                 )
#                 return True
#         return super().editorEvent(event, model, option, index)

#     def checkboxRect(self, option):
#         # 计算复选框的位置
#         checkbox_size = QApplication.style().pixelMetric(QStyle.PM_IndicatorWidth)
#         checkbox_rect = QRect(
#             option.rect.x() + option.rect.width() - checkbox_size - 2,
#             option.rect.y() + (option.rect.height() - checkbox_size) // 2,
#             checkbox_size,
#             checkbox_size,
#         )
#         return checkbox_rect


# class CheckableFileSystemModel(QFileSystemModel):
#     def __init__(self, *args, **kwargs):
#         super(CheckableFileSystemModel, self).__init__(*args, **kwargs)
#         self.checks = {}

#     def data(self, index, role=Qt.DisplayRole):
#         if role == Qt.CheckStateRole and index.column() == 0:
#             return self.checks.get(index, Qt.Unchecked)
#         return super(CheckableFileSystemModel, self).data(index, role)

#     def setData(self, index, value, role=Qt.CheckStateRole):
#         if role == Qt.CheckStateRole and index.column() == 0:
#             self.checks[index] = value
#             self.dataChanged.emit(index, index, [role])
#             return True
#         return super(CheckableFileSystemModel, self).setData(index, value, role)

#     def flags(self, index):
#         return (
#             super(CheckableFileSystemModel, self).flags(index) | Qt.ItemIsUserCheckable
#         )


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.screen = QDesktopWidget().screenGeometry()
        self.setupUi(self)
        # 界面初始大小
        # self.resize(self.screen.width(), self.screen.height() - 75)
        self.socre_records = {}
        self.path = "D:/Desktop/交大操作系统实验/学生报告/02"
        self.filename = os.path.join(self.path, "records.json")
        self.fileList.model = QFileSystemModel()
        self.fileList.model.setRootPath(self.path)
        self.page = 0
        self.total_page = 0
        self.cur_fpath = ""

        # self.model = CheckableFileSystemModel()
        # self.model.setRootPath(self.path)

        # self.fileList.setModel(self.model)
        # self.fileList.setItemDelegate(CheckBoxDelegate(self.fileList))
        # self.fileList.setRootIndex(self.model.index(self.path))

        # 为控件添加模式。
        self.fileList.setModel(self.fileList.model)
        self.fileList.setRootIndex(
            self.fileList.model.index(self.path)
        )  # 只显示设置的那个文件路径。
        self.fileList.doubleClicked.connect(self.set_labinfo)  # 双击文件打开
        self.okBtn.clicked.connect(self.save_score)
        self.exportBtn.clicked.connect(self.save)
        self.initUi()
        self.selModeBox.currentIndexChanged.connect(self.selectionChanged)

    def initUi(self):
        # 属性点 1
        self.coord = Point(0, 0)
        # 初始化
        self.crow = Point(-1, -1)
        # 需要改进，只允许打开一本书
        # 列表
        self.size = Size(2.6, 2.6)
        sel_action = [0, 1, 2, 3]
        for sa in sel_action:
            self.selModeBox.addItem(str(sel_action[sa]))
        # self.selModeBox.setText(None)
        self.Comments.setPlaceholderText("请输入评语")

    def selectionChanged(self, index):
        selected_option = self.selModeBox.itemText(index)
        self.Comments.setText("Selected: " + selected_option)

    def set_labinfo(self, Qmodelidx):
        print(self.fileList.model.filePath(Qmodelidx))  # 输出文件的地址。
        print(self.fileList.model.fileName(Qmodelidx))  # 输出文件名
        fname = self.fileList.model.filePath(Qmodelidx)
        self.cur_fpath = fname
        filename = self.fileList.model.fileName(Qmodelidx)
        fileinfo = Handle().splittitle(filename)
        self.score.setText(str(0))
        self.stuName.setText(fileinfo["name"])
        self.stuID.setText(fileinfo["stuid"])
        self.labName.setText("实验" + fileinfo["labinfo"])
        self.read_book(fname)
        # self.set_page()
        print(fileinfo)

    def get_score(self) -> int:
        return self.score.text()

    def get_stuid(self) -> str:
        return self.stuID.text()

    def get_stuname(self) -> str:
        return self.stuName.text()

    def get_labinfo(self) -> str:
        return self.labName.text()

    def save_score(self):
        stuname = self.get_stuname()
        stuid = self.get_stuid()
        labinfo = self.get_labinfo()
        score = self.get_score()
        self.socre_records[stuid] = tuple((stuname, score, labinfo))
        print(self.socre_records)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.socre_records, f, ensure_ascii=False, indent=4)

    def read_book(self, fname):
        # self.close()
        # 内存有可能泄露
        doc = fitz.open(fname)
        self.total_page = doc.page_count
        vbox = self.book_area(doc.load_page(self.page))
        doc.close()
        layout = self.contentWidget.layout()
        if layout:
            self.remove_layout(layout)
        self.contentWidget.update()
        self.book_add_tab(vbox)

    def remove_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            layout.deleteLater()

    def book_add_tab(self, vbox):
        # tab = QWidget()
        # self.contentWidget.update()
        self.contentWidget.setLayout(vbox)
        # self.contentWidget.update()

        # tab 为页面，title 为标签名称
        # self.contentWidget.addTab(tab, title)
        # self.contentWidget.setCurrentIndex(self.contentWidget.count() - 1)

    def book_area(self, page):
        label = self.page_pixmap(page)
        area = MyArea(self)
        # area.init(self)
        area.setWidget(label)
        # area.sebook(self.get_read_book())

        vbox = QVBoxLayout()
        vbox.addWidget(area)
        return vbox

    def page_pixmap(self, page):
        # 在标签上显示图片
        label = QLabel(self)
        label.setScaledContents(True)
        # 按屏幕大小缩放标签
        # print(self.screen)
        # p.scaled(self.boxsize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        p = render_pdf_page(page, x=self.size.x, y=self.size.y)
        pixmap = QPixmap(p)
        scaled_pixmap = pixmap.scaled(
            self.contentWidget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # 在标签上设置缩放后的图片
        label.setPixmap(scaled_pixmap)
        return label

    def set_current_page(self, right):
        # book = self.get_read_book()
        # 之后统一在 book 中
        if right and self.page < self.total_page:
            # if right:
            self.page += 1

        elif not right and self.page:
            self.page -= 1

    def switch_page(self, right=True):
        self.set_current_page(right)
        self.set_page()

    def set_page(self):
        # book = self.get_read_book()
        # 加载页面
        doc = fitz.open(self.cur_fpath)
        page = doc.load_page(self.page)
        # 获取当前 Widget
        tab = self.contentWidget
        # 获取当前的 Layout
        layout = tab.layout()
        # 获取 Layout 上的控件
        widget = layout.itemAt(0).widget()
        # 获取已经绘制好的 label 对象
        label = self.page_pixmap(page)
        # 将 widget 的内容更改为现在的 label 对象
        doc.close()
        widget.setWidget(label)

    def zoom_book(self, plus=True):
        if plus:
            self.size.x += 0.4
            self.size.y += 0.4
            self.set_page()
        elif not plus:
            self.size.x -= 0.4
            self.size.y -= 0.4
            self.set_page()


# 显示 PDF 封面
def render_pdf_page(page_data, x=1, y=1):
    # 图像缩放比例

    zoom_matrix = fitz.Matrix(x, y)

    # 获取封面对应的 Pixmap 对象
    # alpha 设置背景为白色
    pagePixmap = page_data.get_pixmap(matrix=zoom_matrix, alpha=False)
    # 获取 image 格式
    imageFormat = QImage.Format_RGB888
    # 生成 QImage 对象
    pageQImage = QImage(
        pagePixmap.samples,
        pagePixmap.width,
        pagePixmap.height,
        pagePixmap.stride,
        imageFormat,
    )
    # 生成 pixmap 对象
    pixmap = QPixmap()
    pixmap.convertFromImage(pageQImage)
    return pixmap


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
