from src.crawling.common import refined_text_folder
from src.analysis.util.parser import parse_ch_num
from src.analysis.util.parser import parse_alcohol
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import json
import re
import os

json_folder = refined_text_folder + 'json/'
json_list = {}
for file in os.listdir(json_folder):
    if file.endswith('json'):
        try:
            json_list[file] = json.load(open(json_folder + file, 'r'))
        except json.decoder.JSONDecodeError:
            print(file)


def find_alcohol():
    accu_freq_dict = {}
    res_list = []

    for j in json_list.items():
        n = j[0]
        j = j[1]
        if not j['时间'].startswith('2021'):
            continue
        accu = j['罪名']
        accu_freq_dict[accu] = accu_freq_dict.get(accu, 0) + 1
        if not accu.startswith('危险驾驶'):
            continue

        fine = j['附加刑']
        alcohol = j['酒精含量']
        if fine == 'None' or alcohol == 'None':
            continue
        amount = parse_alcohol(alcohol)
        fine_num = parse_ch_num(fine)
        if fine_num != -1:
            res_list.append([j['时间'], j['省份'][:3], amount, fine_num, n])

    return sorted(sorted(res_list, key=lambda x: x[3], reverse=True), key=lambda x: x[0], reverse=True)


def run():
    a = find_alcohol()      # 时间 : 省份 : 酒精 : 附加刑 : 标题
    yax = []
    xax = []
    for l in a:
        yax.append(l[3])
        xax.append(l[2])
    plt.scatter(xax, yax)
    plt.show()


if __name__ == '__main__':
    run()
