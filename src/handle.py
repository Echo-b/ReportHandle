import os
import re

# 确保 QFileSystemModel 查找出的文件模型显示出的文件与Windows资源管理器中显示的保持一致
# reference : https://ocsxxi.top/posts/2024-01-13-1/
from natsort import os_sorted

class Handle:
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
    
    def splittitle(self, filename: str) -> dict:
        expected_pattern = (
            r"^(?P<name>.+)-(?P<student_id>\d+)-实验(?P<experiment_num>\d+|一)\.pdf$"
        )
        expected_match = re.match(expected_pattern, filename)

        fileinfo = {}
        if expected_match:
            fileinfo["name"] = expected_match.group("name")
            fileinfo["stuid"] = expected_match.group("student_id")
            fileinfo["labinfo"] = expected_match.group("experiment_num")
            print(expected_match.group("name"))
        return fileinfo
