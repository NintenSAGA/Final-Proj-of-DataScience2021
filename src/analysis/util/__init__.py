import json
import os

from src.analysis.util.parser import *


def json_reader(folder: str) -> list:
    """
    从指定文件夹中读取全部json，返回list[dict]
    :param folder:
    :return:
    """
    if not os.path.exists(folder):
        raise FileNotFoundError('"{}"不存在！'.format(folder))
    if not folder.endswith('/'):
        folder += '/'
    ret = []
    for file_name in os.listdir(folder):
        if not file_name.endswith('.json'):
            continue
        full_path = folder + file_name
        try:
            ret.append(json.load(open(full_path, 'r')))
        except json.decoder.JSONDecodeError:
            print(full_path)
    return ret


def percentage(numerator, denominator) -> str:
    """
    计算百分数
    :param numerator:
    :param denominator:
    :return:
    """
    if denominator == 0:
        return "0.00%"
    return "%.2f" % (float(numerator) / float(denominator) * 100) + '%'


def table_generator(header: list, contents: list) -> str:
    """
    生成Markdown表格
    :param header:
    :param contents:
    :return:
    """
    width = len(header)
    ret = []
    for line in [header, ['---' for _ in range(width)]] + contents:
        ret.append('| {} |'.format(' | '.join(line)))
    return os.linesep.join(ret)
