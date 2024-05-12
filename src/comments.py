import json
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QButtonGroup
from PyQt5.QtGui import  QIcon
from Ui_commentsWindow import Ui_Dialog
from datahandle import DataHandle
                            
class CommentTemplate(QDialog, Ui_Dialog):
    get_data_signal = pyqtSignal(list) #子界面类创建信号用来绑定主界面类的函数方法
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./image/avatar.jpg'))
        self.setWindowTitle("评语选择模板")
        self.init_params()
        self.creat_groups()
        self.init_slots()

    def init_slots(self):
        self.clsOptionsBtn.clicked.connect(self.cancel_select)
        self.ensureOptionsBtn.clicked.connect(self.confirm_select)

    def creat_groups(self):
        self.group1 = QButtonGroup(self)
        self.group1.setExclusive(True)
        self.group1.addButton(self.docBasic)
        self.group1.addButton(self.docGood)
        self.group1.addButton(self.docGreat)
        self.group1.addButton(self.docExcellent)

        self.group2 = QButtonGroup(self)
        self.group2.setExclusive(True)
        self.group2.addButton(self.compBasic)
        self.group2.addButton(self.compGood)
        self.group2.addButton(self.compGreat)
        self.group2.addButton(self.compExcellent)

        self.group3 = QButtonGroup(self)
        self.group3.setExclusive(True)
        self.group3.addButton(self.readBasic)
        self.group3.addButton(self.readGood)
        self.group3.addButton(self.readGreat)
        self.group3.addButton(self.readExcellent)

        self.group4 = QButtonGroup(self)
        self.group4.setExclusive(True)
        self.group4.addButton(self.refBasic)
        self.group4.addButton(self.refGood)
        self.group4.addButton(self.refGreat)
        self.group4.addButton(self.refExcellent)

    def get_key(self, key: str) -> str:
        # 定义两个列表
        english_levels = ['basic', 'good', 'great', 'excellent']
        chinese_levels = ['一般', '好', '较好', '优秀']

        idx = chinese_levels.index(key)
        return english_levels[idx]

    def init_params(self):
        self.options = []
        self.path = './template/comments.json'
        self.DH = DataHandle()
        self.templates = self.DH.load_data(self.path)
    
    def cancel_select(self):
        for bt1 in self.group1.buttons():
            bt1.setChecked(False)
        for bt2 in self.group2.buttons():
            bt2.setChecked(False)
        for bt3 in self.group3.buttons():
            bt3.setChecked(False)
        for bt4 in self.group4.buttons():
            bt4.setChecked(False)

    def confirm_select(self):
        self.options = []
        self.options.append(self.templates.get('document_naming_standard', {}).get(self.get_key(self.group1.checkedButton().text()), "没有找到合适的"))
        self.options.append(self.templates.get('report_completeness', {}).get(self.get_key(self.group2.checkedButton().text()), "没有找到合适的"))
        self.options.append(self.templates.get('readability_of_insights', {}).get(self.get_key(self.group3.checkedButton().text()), "没有找到合适的"))
        self.options.append(self.templates.get('reference_value', {}).get(self.get_key(self.group4.checkedButton().text()), "没有找到合适的"))
        print(self.options)
        self.get_data_signal.emit(self.options)
        

    def get_input(self) ->  list:
        if self.options:
            return self.options

        
