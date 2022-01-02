import re

pat_s = '[{}|\d]+'

n2han = {
    0: '零',
    1: '一壹',
    2: '二两',
    3: '三',
    4: '四',
    5: '五',
    6: '六',
    7: '七',
    8: '八',
    9: '九',
    10: '十',
    100: '百佰',
    1000: '千仟',
    10000: '万',
    100000000: '亿'
}
han2n = {}
han_t = ''
for item in n2han.items():
    for han in item[1]:
        han_t += han
        han2n[han] = item[0]

pat = re.compile(r'{}'.format(pat_s.format(han_t)))


def parse_ch_num(word: str) -> int:
    """
    解析中文数字，返回int值
    当字符串中不含数字时，返回 ValueError
    :param word: 中文数字
    :return:
    """
    word = word.strip()

    match = pat.search(word)

    if not match:
        print('错误：{}无法找到数字'.format(word))
        raise ValueError

    num_s = pat.search(word).group(0)

    try:
        return int(num_s)
    except ValueError:
        try:
            # 预处理
            if han2n.get(num_s[0], 0) >= 10:
                num_s = '一' + num_s
            # 处理
            num = 0
            unit = 1
            for c in num_s[::-1]:
                if c.isdigit():     # case 1: 是阿拉伯数字
                    num += unit * int(c)
                    unit *= 10
                else:               # case 2: 是汉字
                    n = han2n.get(c)
                    if n >= 10:
                        unit *= n if unit == 1 else 10
                    else:
                        num += unit * n
            return num
        except (TypeError, ValueError):
            print('错误：{} 中含不支持的汉字'.format(num_s))
            return -1


if __name__ == '__main__':
    print(parse_ch_num('500万'))