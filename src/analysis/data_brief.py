from src.analysis import util, json_folder


def show_brief(year: str) -> list:
    """
    显示这一年的信息概览，包含
    年份 文书总数 危险驾驶总数 危险驾驶占比 醉驾总数 醉驾占危险驾驶占比
    :param year: 年份
    :return: 包含以上信息的列表
    """
    return show_brief_with_given(util.json_reader(json_folder + year), year)


def show_brief_with_given(raw_list: list, title: str) -> list:
    n0 = len(raw_list)
    ret = [title, str(n0)]   # 年份，文书总数

    dangerous_list = list(filter(lambda x: x['罪名'].startswith('危险驾驶'), raw_list))
    n1 = len(dangerous_list)
    ret.append(str(n1))     # 危险驾驶总数
    ret.append(util.percentage(n1, n0))   # 危险驾驶占比

    drunk_list = list(filter(lambda x: x['酒精含量'] != 'None', dangerous_list))
    n2 = len(drunk_list)
    ret.append(str(n2))     # 醉驾总数
    ret.append(util.percentage(n2, n1))     # 醉驾占危险驾驶占比

    return ret


def region_brief(year: str, sort_key: int = 0) -> list:
    """
    显示这一年不同地区的案件分布情况
    省级行政区 文书总数 危险驾驶总数 危险驾驶占比 醉驾总数 醉驾占危险驾驶占比
    :param sort_key: 0, 1, ..., 4: 文书总数, ..., 醉驾占危险驾驶占比
    :param year:
    :return:
    """
    raw_list = util.json_reader(json_folder + year)
    prov_set = set()
    for case in raw_list:
        prov = case['省份']
        if prov == 'None':
            continue
        prov_set.add(prov[:2])
    ret = []
    for prov in prov_set:
        ret.append(show_brief_with_given(list(filter(lambda x: x['省份'].startswith(prov), raw_list)), prov))
    return sorted(filter(lambda x: int(x[1]) >= 162, ret), key=lambda x: float(x[1 + sort_key].strip('%')), reverse=True)


def crime_brief(year: str) -> list:
    """
    显示这一年不同罪名的案件分布情况
    排名 罪名 数量 占比
    :param year:
    :return:
    """
    raw_list = util.json_reader(json_folder + year)
    n0 = len(raw_list)
    crime_dict = {}
    for case in raw_list:
        crime = case['罪名']
        temp = crime_dict.get(crime, 0)
        crime_dict[crime] = temp + 1
    ret = []
    for i, crime_tuple in enumerate(sorted(crime_dict.items(), key=lambda x: x[1], reverse=True), start=1):
        n1 = crime_tuple[1]
        ret.append([str(i), crime_tuple[0], str(n1), util.percentage(n1, n0)])
    return ret


if __name__ == '__main__':
    # year_list = [show_brief(year) for year in '2020 2021'.split()]
    # print(util.table_generator('年份 文书总数 危险驾驶总数 危险驾驶占比 醉驾总数 醉驾占危险驾驶占比'.split(), year_list))
    # print(util.table_generator('排名 罪名 数量 占比'.split(), crime_brief('2021')))
    print(util.table_generator('省级行政区 文书总数 危险驾驶总数 危险驾驶占比 醉驾总数 醉驾占危险驾驶占比'.split(), region_brief('2021', 2)))