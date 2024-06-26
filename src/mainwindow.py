import sys
import os
import json
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileSystemModel,
    QDialog,
    QVBoxLayout,
    QLabel,
    QFileDialog,
)
from qfluentwidgets import MessageBox, TeachingTip, TeachingTipTailPosition, InfoBarIcon

from PyQt5.QtGui import QImage, QPixmap, QIcon
from Ui_MainWindow import Ui_MainWindow
from filehandle import Handle
from Area import MyArea
from utils import Size, Point
from comments import CommentTemplate
from datahandle import DataHandle

try:
    import fitz
except ImportError:
    print("请安装 fitz")


class MainWindow(QMainWindow, Ui_MainWindow):
    get_select_options_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 界面初始大小
        # self.resize(self.screen.width(), self.screen.height())
        self.setWindowIcon(QIcon("./image/avatar.jpg"))
        self.setWindowTitle("简易报告批改器")
        # self.resize(1080,800)
        self.initSlots()
        self.ctw = CommentTemplate()
        self.get_select_options_signal.connect(self.ctw.confirm_select)

    def initUi(self):
        # 属性点 1
        self.coord = Point(0, 0)
        # 初始化
        self.crow = Point(-1, -1)
        # 需要改进，只允许打开一本书
        # 列表
        self.size = Size(2.6, 2.6)
        # sel_action = [0, 1, 2, 3]
        # for sa in sel_action:
        #     self.selModeBox.addItem(str(sel_action[sa]))
        # self.selModeBox.setText(None)
        self.Comments.setPlaceholderText("请输入评语")
        self.fileList.model = QFileSystemModel()
        self.fileList.model.setRootPath(self.path)
        # 为控件添加模式。
        # 设置过滤器，仅显示 PDF 文件
        self.fileList.model.setNameFilters(["*.pdf"])
        self.fileList.model.setNameFilterDisables(
            False
        )  # 禁用未匹配名称过滤器的文件的显示
        self.fileList.setModel(self.fileList.model)
        self.fileList.setRootIndex(
            self.fileList.model.index(self.path)
        )  # 只显示设置的那个文件路径。
        # self.set_page()
        self.read_book(self.cur_fpath)
        self.set_stuinfo(self.cur_fname)

    def get_sel_fpath(self):
        # 打开文件夹选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(
            self, "请选择文件夹路径", options=options
        )
        if folder:
            self.path = folder
            self.initParmas()
            self.initUi()
        else:
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.ERROR,
                title="提示",
                content="打开文件夹失败",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )

    def initParmas(self):
        self.socre_records = {}
        self.options = []
        # self.path = "C:/Users/EchoBai/Desktop/操作系统实验报告/00"
        self.filename = os.path.join(self.path, "records.json")
        self.pdflist = Handle().findlist(self.path)
        print(self.pdflist)
        if self.pdflist:
            self.init_score_records()
            self.page = 0
            self.total_page = 0
            self.cur_fname = self.pdflist[self.page]
            self.cur_fpath = self.path + "/"
            self.cur_fpath += self.cur_fname
            self.index = 0
        else:
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.INFORMATION,
                title="提示",
                content="所选文件夹没有找到pdf文件",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )

    def init_score_records(self):
        for fname in self.pdflist:
            fileinfo = Handle().splittitle(fname)
            if fileinfo:
                sname = fileinfo["name"]
                stuid = fileinfo["stuid"]
                score = "0"
                comments = ""
                labinfo = "实验" + str(fileinfo["labinfo"])
                self.socre_records[stuid] = tuple((sname, score, labinfo, comments))
            else:
                TeachingTip.create(
                    target=self,
                    icon=InfoBarIcon.ERROR,
                    title="提示",
                    content=str(fileinfo) + "文件命名格式不匹配",
                    isClosable=True,
                    tailPosition=TeachingTipTailPosition.BOTTOM,
                    duration=2000,
                    parent=self,
                )

    def initSlots(self):
        self.fileList.doubleClicked.connect(self.open_file)  # 双击文件打开
        self.okBtn.clicked.connect(self.save_score)
        self.exportBtn.clicked.connect(self.save)
        self.preDocBtn.clicked.connect(self.pre_doc)
        self.nextDocBtn.clicked.connect(self.next_doc)
        self.selCommentsTemplate.clicked.connect(self.select_comments_template)
        self.openFileAction.triggered.connect(self.get_sel_fpath)
        self.writeExcelAction.triggered.connect(self.write_data_to_excel)

    def write_data_to_excel(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fpath, _ = QFileDialog.getOpenFileName(
            self,
            "请选择需要导入的excel名单表",
            "",
            "Excel Files (*.xlsx *.xls)",
            options=options,
        )
        if fpath:
            DataHandle().write_to_excel(fpath, self.socre_records)
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.SUCCESS,
                title="提示",
                content="写入成绩成功",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )
        else:
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.INFORMATION,
                title="提示",
                content="请选择文件",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )

    def select_comments_template(self):
        self.show_comments_windos()

    def show_comments_windos(self):
        self.ctw.show()
        self.ctw.get_data_signal.connect(self.get_data)

    def get_data(self, data: list):
        self.options = data
        print(self.options)
        if self.options is not None:
            self.Comments.clear()
            for op in self.options:
                self.Comments.append(op)
        self.ctw.close()

    def update_params(self, fname):
        self.cur_fname = fname
        self.cur_fpath = self.path + "/"
        self.cur_fpath += self.cur_fname
        self.page = 0

    def next_doc(self):
        next_fname = self.get_next_file()
        self.update_params(next_fname)
        # self.read_book(self.cur_fpath)
        self.set_stuinfo(next_fname)
        self.set_page()

    def pre_doc(self):
        pre_fname = self.get_pre_file()
        self.update_params(pre_fname)

        # self.read_book(self.cur_fpath)
        self.set_page()
        self.set_stuinfo(pre_fname)

    def open_file(self, Qmodelidx):
        print(self.fileList.model.filePath(Qmodelidx))  # 输出文件的地址。
        print(self.fileList.model.fileName(Qmodelidx))  # 输出文件名
        fpath = self.fileList.model.filePath(Qmodelidx)
        fname = self.fileList.model.fileName(Qmodelidx)
        self.cur_fpath = fpath
        self.cur_fname = fname
        self.index = self.pdflist.index(fname)
        filename = self.fileList.model.fileName(Qmodelidx)
        self.set_stuinfo(filename)
        # self.read_book(fpath)
        self.page = 0
        self.set_page()

    def set_stuinfo(self, filename):
        fileinfo = Handle().splittitle(filename)
        self.stuName.setText(fileinfo["name"])
        stuid = fileinfo["stuid"]
        self.stuID.setText(stuid)
        if self.socre_records[stuid] is not None:
            self.score.setText(str(self.socre_records[stuid][1]))
        else:
            self.score.setText(str(0))
        self.labName.setText("实验" + str(fileinfo["labinfo"]))

    def get_score(self) -> int:
        return self.score.text()

    def get_stuid(self) -> str:
        return self.stuID.text()

    def get_stuname(self) -> str:
        return self.stuName.text()

    def get_labinfo(self) -> str:
        return self.labName.text()

    def get_next_file(self) -> str:
        if self.index == len(self.pdflist) - 1:
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.INFORMATION,
                title="提示",
                content="恭喜你，已经全部批改完毕！！！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )
            self.index = len(self.pdflist) - 1
        elif self.index < len(self.pdflist) - 1:
            self.index += 1
        return self.pdflist[self.index]

    def get_pre_file(self) -> str:
        if self.index == 0:
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.INFORMATION,
                title="提示",
                content="当前已经是第一篇了",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )
            self.index = 0
        elif self.index > 0:
            self.index -= 1
        return self.pdflist[self.index]

    def save_score(self):
        stuname = self.get_stuname()
        stuid = self.get_stuid()
        labinfo = self.get_labinfo()
        score = self.get_score()
        comments = self.Comments.toPlainText()
        self.socre_records[stuid] = tuple((stuname, score, labinfo, comments))
        # self.socre_records[stuid][1] = score
        # self.socre_records[stuid][3] = comments
        TeachingTip.create(
            target=self,
            icon=InfoBarIcon.SUCCESS,
            title="提示",
            content="评分成功",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self,
        )
        print(self.socre_records)
        self.next_doc()

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.socre_records, f, ensure_ascii=False, indent=4)
        TeachingTip.create(
            target=self,
            icon=InfoBarIcon.SUCCESS,
            title="提示",
            content="导出文件成功",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self,
        )

    def read_book(self, fname):
        # self.close()
        # 内存有可能泄露
        doc = fitz.open(fname)
        self.total_page = doc.page_count
        vbox = self.book_area(doc.load_page(self.page))
        doc.close()
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
        if self.contentWidget.layout() is not None:
            self.contentWidget.layout().deleteLater()
        self.contentWidget.setLayout(vbox)
        self.contentWidget.update()

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
        p = render_pdf_page(page, x=self.size.x, y=self.size.y)
        pixmap = QPixmap(p)
        # 按控件大小缩放标签
        scaled_pixmap = pixmap.scaled(
            self.contentWidget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # 在标签上设置缩放后的图片
        label.setPixmap(scaled_pixmap)
        return label

    def set_current_page(self, right):
        # book = self.get_read_book()
        # 之后统一在 book 中
        if right and self.page < (self.total_page - 1):
            # if right:
            self.page += 1

        elif right and self.page == (self.total_page - 1):
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.INFORMATION,
                title="提示",
                content="已经是最后一页啦！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )
            self.page = self.total_page - 1

        elif not right and self.page:
            self.page -= 1
        elif not right and self.page == 0:
            TeachingTip.create(
                target=self,
                icon=InfoBarIcon.INFORMATION,
                title="提示",
                content="已经是第一页啦！",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self,
            )
            self.page = 0

    def switch_page(self, right=True):
        self.set_current_page(right)
        self.set_page()

    def set_page(self):
        # book = self.get_read_book()
        # 加载页面
        doc = fitz.open(self.cur_fpath)

        self.total_page = doc.page_count

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
