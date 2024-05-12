import json
import pandas as pd

class DataHandle(object):
    def __init__(self) -> None:
        pass
    def load_data(self, filename) ->dict:
        # 使用json.dump()保存字典到文件
        self.stutable = {}
        with open(filename, 'r', encoding='utf-8') as f:
            self.stutable = json.load(f)
        return self.stutable
    def printData(self):
        print(self.stutable)


    def write_to_excel(self, fepath, data):
        df = pd.read_excel(fepath)
        df['学号'] = df['学号'].astype(str)
        for key, value in data.items():
            experiment = value[2]  # 实验名称
            # labcomments = "实验评价"
            # comments = value[3] # 实验评价值
            score = value[1]       # 分数

        # 检查是否存在对应的实验列，如果不存在则创建
            if experiment not in df.columns:
                df[experiment] = pd.NA  # 新建列，初始填充为NA
            # if labcomments not in df.columns:
            #     df[labcomments] = pd.NA

        # 找到对应学号的行
            if key in df['学号'].values:
                df.loc[df['学号'] == key, experiment] = score
                # df.loc[df['学号'] == key, labcomments] = comments
        # 显示结果
        print(df)
        df.to_excel(fepath, index=False)
