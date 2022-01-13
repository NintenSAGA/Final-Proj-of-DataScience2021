from src.analysis.util.parser import parse_ch_num
import re

units = [
    ['年', 365],
    ['月', 30],
    ['周', '星期', 7],
    ['日', '天', 1]
]


def parse_penalty(words: str) -> int:
    """
    获取主刑信息
    :param words:
    :return: 单位：日
    """
    words = words.strip()
    backup = words
    # 特殊处理
    if re.search(r'(死刑|无期徒刑)', words):
        return 100 * 365

    time = 0
    for unit_set in units:
        for unit in unit_set[:-1]:
            if unit not in words:
                continue
            words_set = words.split(unit)
            left = words_set[0]
            time += parse_ch_num(left) * unit_set[-1]
            words = str(words_set[1:]) if len(words_set) > 1 else ''
            break
        if words == '':
            break
    if time >= 5000:
        print('{}识别成了{}'.format(backup, time))
    return time



