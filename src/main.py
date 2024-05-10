from datahandle import DataHandle

def main():
    path = "C:/Users/EchoBai/Desktop/操作系统实验报告/02" + "/records.json"
    DH = DataHandle()
    DH.load_data(path)
    DH.printData()

if __name__ == '__main__':
    main()