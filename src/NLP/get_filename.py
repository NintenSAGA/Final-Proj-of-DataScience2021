import os


def get_all(path):
    result = []
    dir_list = os.listdir(path)
    for p in dir_list:
        sub_dir = os.path.join(path, p)
        if os.path.isdir(sub_dir):
            get_all(sub_dir)
        else:
            result.append(sub_dir)
    return result