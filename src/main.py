from datahandle import DataHandle

def main():
    path = "./template/comments.json"
    DH = DataHandle()
    comments = DH.load_data(path)
    values = ['Basic','Good', 'Great', 'Excellent']
    print(comments.get('document_naming_standard', {}).get('good', "没有找到合适的"))
    # DH.printData()

if __name__ == '__main__':
    main()