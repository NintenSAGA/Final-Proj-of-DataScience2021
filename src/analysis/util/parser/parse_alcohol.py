import re

pat = re.compile('[\\d|\\.]+')


def parse_alcohol(word: str) -> float:
    """
    解析酒精含量，返回 n mg/ml
    :param word:
    :return:
    """
    candidates = pat.findall(word)
    if candidates:
        try:
            f1 = float(candidates[0])
            f2 = float(candidates[1]) if len(candidates) > 1 else 1
            amount = f1 * 100 / f2
            if amount > 1000:
                amount /= 100
            return amount
        except ValueError:
            print('错误：{}中数字格式似乎存在问题'.format(word))
            return -1
    else:
        print('错误：{}中找不到酒精含量'.format(word))
        return -1
