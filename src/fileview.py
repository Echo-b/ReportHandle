import sys
from PyQt5.QtWidgets import QTreeView,QApplication, QFileSystemModel
from PyQt5.QtGui import *



class TreeViewDemo(QTreeView):
    def __init__(self, parent=None):
        super(TreeViewDemo, self).__init__(parent)
    
        #window系统提供的模式
        path = 'C:/Users/EchoBai/Desktop/操作系统实验报告/02'
        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        
        #为控件添加模式。
        self.setModel(self.model)
        self.setRootIndex(self.model.index(path)) #只显示设置的那个文件路径。
        self.doubleClicked.connect(self.file_name) #双击文件打开
        self.setWindowTitle("QTreeView例子")
        self.resize(640,480)
    
    def file_name(self,Qmodelidx):
        print(self.model.filePath(Qmodelidx))  #输出文件的地址。
        print(self.model.fileName(Qmodelidx))  #输出文件名
    

if __name__=='__main__':
    app = QApplication(sys.argv)
    tree = TreeViewDemo()
    tree.show()
    sys.exit(app.exec_())
            