import os
import re

# 确保 QFileSystemModel 查找出的文件模型显示出的文件与Windows资源管理器中显示的保持一致
# reference : https://ocsxxi.top/posts/2024-01-13-1/
from natsort import os_sorted


class Handle(object):
    def __init__(self) -> None:
        pass

    def findlist(self, path: str) -> list:
        fl = []
        # 获取文件列表，忽略大小写进行排序
        pathlist = os_sorted(os.listdir(path))
        for filename in pathlist:
            if os.path.splitext(filename)[1].lower() == ".pdf":
                fl.append(filename)
        return fl

    def convert_chinese_number(self, num_str):
        chinese_to_arabic = {
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
        }
        # 检查字符串是否全为汉字，如果是则转换为阿拉伯数字
        if all(char in chinese_to_arabic for char in num_str):
            if len(num_str) == 1:
                return chinese_to_arabic[num_str]
            elif num_str.startswith("十"):
                return 10 + (chinese_to_arabic[num_str[1]] if len(num_str) > 1 else 0)
            elif num_str.endswith("十"):
                return chinese_to_arabic[num_str[0]] * 10
            else:
                tens = chinese_to_arabic[num_str[0]] * 10
                units = chinese_to_arabic[num_str[2]]
                return tens + units
        return int(num_str)  # 如果是阿拉伯数字字符串，则直接转换为整数

    def splittitle(self, filename: str) -> dict:
        expected_pattern = r"^(?P<name>.+)-(?P<student_id>\d+)-实验(?P<experiment_num>\d+|[一二三四五六七八九十]+)\.pdf$"
        expected_match = re.match(expected_pattern, filename)

        fileinfo = {}
        if expected_match:
            fileinfo["name"] = expected_match.group("name")
            fileinfo["stuid"] = expected_match.group("student_id")
            fileinfo["labinfo"] = self.convert_chinese_number(
                expected_match.group("experiment_num")
            )
            print(expected_match.group("name"))
        return fileinfo
