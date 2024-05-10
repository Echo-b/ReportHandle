import sys
import os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QWidget, QVBoxLayout, QDesktopWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from Ui_MainWindow import Ui_MainWindow
from handle import Handle
from Area import MyArea
from utils import Size, Point

try:
    import fitz
except ImportError:
    print('请安装 fitz')
                            
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.screen = QDesktopWidget().screenGeometry()
        self.setupUi(self)
        self.boxsize = self.contentWidget.size()
        self.socre_records = {}
        self.path = 'C:/Users/EchoBai/Desktop/操作系统实验报告/02'
        self.filename = os.path.join(self.path, "records.json")
        self.fileList.model = QFileSystemModel()
        self.fileList.model.setRootPath(self.path)
        self.page = 0
        self.total_page = 0
        self.cur_fpath = ""
        
        
        #为控件添加模式。
        self.fileList.setModel(self.fileList.model)
        self.fileList.setRootIndex(self.fileList.model.index(self.path)) #只显示设置的那个文件路径。
        self.fileList.doubleClicked.connect(self.set_labinfo) #双击文件打开
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
        sel_action = [0, 1,  2, 3]
        for sa in sel_action:
            self.selModeBox.addItem(str(sel_action[sa]))
        # self.selModeBox.setText(None)
        self.Comments.setPlaceholderText("请输入评语")
   

    def selectionChanged(self, index):
        selected_option = self.selModeBox.itemText(index)
        self.Comments.setText('Selected: ' + selected_option)

    def set_labinfo(self,Qmodelidx):
        print(self.fileList.model.filePath(Qmodelidx))  #输出文件的地址。
        print(self.fileList.model.fileName(Qmodelidx))  #输出文件名
        fname = self.fileList.model.filePath(Qmodelidx)
        self.cur_fpath = fname
        filename = self.fileList.model.fileName(Qmodelidx)
        fileinfo =  Handle().splittitle(filename)
        self.score.setText(str(0))
        self.stuName.setText(fileinfo['name'])
        self.stuID.setText(fileinfo['stuid'])
        self.labName.setText("实验" + fileinfo['labinfo'])
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
        self.socre_records[stuid] =  tuple((stuname,score,labinfo))
        print(self.socre_records)
    
    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
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
        p = render_pdf_page(page, x = self.size.x, y = self.size.y)
        # 按屏幕大小缩放标签
        print(self.screen)
        p.scaled(self.screen.width() / 2, self.screen.height())
        # 在标签上设置图片
        label.setPixmap(QPixmap(p))
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
def render_pdf_page(page_data, x = 1,  y = 1):
    # 图像缩放比例

    zoom_matrix = fitz.Matrix(x, y)

    # 获取封面对应的 Pixmap 对象
    # alpha 设置背景为白色
    pagePixmap = page_data.get_pixmap(
        matrix=zoom_matrix,
        alpha=False)
    # 获取 image 格式
    imageFormat = QImage.Format_RGB888
    # 生成 QImage 对象
    pageQImage = QImage(
        pagePixmap.samples,
        pagePixmap.width,
        pagePixmap.height,
        pagePixmap.stride,
        imageFormat)
    # 生成 pixmap 对象
    pixmap = QPixmap()
    pixmap.convertFromImage(pageQImage)
    return pixmap  
                          
if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()