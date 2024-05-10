import os
import re

class Handle():
    def __init__(self) -> None:
        pass
        
    def findlist(self, path: str)-> list:
        fl = []
        pathlist = os.listdir(path)
        for filename in pathlist:
            if os.path.splitext(filename)[1]==".pdf": 
                fl.append(filename)
        
        return fl
    
    def splittitle(self, filename: str) -> dict:
        expected_pattern = r'^(?P<name>.+)-(?P<student_id>\d+)-实验(?P<experiment_num>\d+|二)\.pdf$'
        expected_match = re.match(expected_pattern, filename)

        fileinfo = {}
        if expected_match:
            fileinfo['name'] = expected_match.group('name')
            fileinfo['stuid'] = expected_match.group('student_id')
            fileinfo['labinfo'] = expected_match.group('experiment_num')
            print(expected_match.group('name'))
        return fileinfo