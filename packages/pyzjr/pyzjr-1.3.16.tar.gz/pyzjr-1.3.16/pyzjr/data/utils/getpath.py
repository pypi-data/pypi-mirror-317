import os
from pathlib import Path

import pyzjr.Z as Z


def getPhotoPath(path, debug=False):
    """
    :param path: 文件夹路径
    :param debug: 开启打印文件名错误的名字
    :return: 包含图片路径的列表
    """
    imgfile = []
    allfile = []
    file_list = os.listdir(path)
    for i in file_list:
        if debug:
            if i[0] in ['n', 't', 'r', 'b', 'f'] or i[0].isdigit():
                print(f"File name error occurred at the beginning of {i}!")
        newph = os.path.join(path, i).replace("\\", "/")
        allfile.append(newph)
        _, file_ext = os.path.splitext(newph)
        if file_ext[1:] in Z.IMG_FORMATS:
            imgfile.append(newph)

    return imgfile, allfile

def SearchFilePath(filedir, format='png'):
    """What is returned is a list that includes all paths under the target path that match the suffix."""
    search_file_path = []
    for root, dirs, files in os.walk(filedir):
        for filespath in files:
            if str(filespath).endswith(format):
                search_file_path.append(os.path.join(root, filespath))
    return search_file_path

def split_path2list(path_str):
    """
    path_list = split_path2list('D:\PythonProject\MB_TaylorFormer\DehazeFormer\data\rshazy\test\GT\220.png')
    Return:
        ['D:\\', 'PythonProject', 'MB_TaylorFormer', 'DehazeFormer', 'data', 'rshazy', 'test', 'GT', '220.png']
    """
    path = Path(path_str)
    path_parts = path.parts
    return list(path_parts)