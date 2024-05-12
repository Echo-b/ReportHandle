import os
import re

# # 指定包含PDF文件的目录
pdf_directory = 'your/path'  # 将此路径替换为实际的目录路径

# 读取文件夹中的所有文件名
filenames = [f for f in os.listdir(pdf_directory) if os.path.isfile(os.path.join(pdf_directory, f))]

# 定义正则表达式
pattern = r'(?P<name>[\u4e00-\u9fa5·\.]+)[\-\+\_]*(?P<student_id>\d+)[\-\+\_]*实验(?P<experiment_number>[0-9一二三四五六七八九十]+)\.pdf$|(?P<student_id2>\d+)[\-\+\_]*(?P<name2>[\u4e00-\u9fa5·\.]+)[\-\+\_]*实验(?P<experiment_number2>[0-9一二三四五六七八九十]+)'


# 函数，用于从文件名中提取信息并重命名文件
def rename_filename(filename):
    match = re.match(pattern, filename)
    if match:
        name = match.group('name') if match.group('name') else match.group('name2')
        student_id = match.group('student_id') if match.group('student_id') else match.group('student_id2')
        experiment_number = match.group('experiment_number') if match.group('experiment_number') else match.group('experiment_number2')
        new_filename = f"{name}-{student_id}-实验{experiment_number}.pdf"
        return new_filename
    else:
        return None

# 遍历文件名并重命名
for filename in os.listdir(pdf_directory):
    full_path = os.path.join(pdf_directory, filename)
    if os.path.isfile(full_path):
        new_name = rename_filename(filename)
        if new_name:
            new_path = os.path.join(pdf_directory, new_name)
            os.rename(full_path, new_path)
            print(f"重命名成功: {filename} -> {new_name}")
        else:
            print(f"无法匹配，未重命名: {filename}")