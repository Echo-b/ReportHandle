import json

class DataHandle(object):
    def __init__(self) -> None:
        self.records = {}
    def load_data(self, filename):
        # 使用json.dump()保存字典到文件
        with open(filename, 'r', encoding='utf-8') as f:
            self.records = json.load(f)
    def printData(self):
        print(self.records)
