import json

class DataHandle(object):
    def __init__(self) -> None:
        pass
    def load_data(self, filename) ->dict:
        # 使用json.dump()保存字典到文件
        self.records = {}
        with open(filename, 'r', encoding='utf-8') as f:
            self.records = json.load(f)
        return self.records
    def printData(self):
        print(self.records)
