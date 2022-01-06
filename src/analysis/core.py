from src.crawling.common import refined_text_folder
from src.analysis.util.parser import parse_ch_num, parse_alcohol, parse_penalty
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
import json
import re
import os

json_folder = refined_text_folder + 'json/'
json_list = {}
for file in os.listdir(json_folder):
    if file.endswith('json'):
        try:
            json_list[''.join(file.split('.')[:3])] = json.load(open(json_folder + file, 'r'))
        except json.decoder.JSONDecodeError:
            print(file)


def parse_numeric_info():
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

        penalty = j['主刑']
        fine = j['附加刑']
        alcohol = j['酒精含量']
        j['附加刑'] = parse_ch_num(fine) if fine != 'None' else 0
        j['酒精含量'] = parse_alcohol(alcohol) if alcohol != 'None' else 0
        j['主刑'] = parse_penalty(penalty) if penalty != 'None' else 0
        j['案件索引'] = n
        res_list.append(j)
    return res_list


def run():
    df = pd.DataFrame(parse_numeric_info())
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # df = df.loc[:, ['省份', '主刑', '附加刑', '酒精含量', '案件索引']]
    df = df[df['酒精含量'] >= 80]
    df = df[df['主刑'] <= 200]
    df = df[df['附加刑'] < 12000]
    df = df[df['省份'] == '广东省']      # type: pd.DataFrame
    df = df.reset_index(drop=True)

    # Get Unique continents
    color_labels = df['省份'].unique()

    # List of colors in the color palettes
    rgb_values = sns.color_palette("Set2", len(df['省份']))

    # Map continents to the colors
    color_map = dict(zip(color_labels, rgb_values))

    plt.rcParams["font.family"] = "Hei"

    df.plot.scatter('酒精含量', '附加刑', c=df['省份'].map(color_map))
    df.plot.scatter('酒精含量', '主刑', c=df['省份'].map(color_map))
    df.plot.scatter('酒精含量', '附加刑', '主刑', c='主刑', cmap='coolwarm')

    alc = df.get('酒精含量')
    a2d = df.loc[:, ['主刑', '附加刑']]
    a1d = do_pca(a2d)

    scatter_draw(alc, a1d)


def do_pca(array):
    r = array.sum()[1] / array.sum()[0]
    array = array.dot(np.array([[1, 0], [0, 1/r]]))
    pca = PCA(1)
    pca.fit(array)
    return pca.transform(array)


def scatter_draw(a1, a2):
    fig, ax = plt.subplots()
    plt.rcParams["font.family"] = "Hei"
    ax.scatter(a1, a2)
    ax.set_xlabel('酒精含量')
    ax.set_ylabel('主刑与附加刑的线性组合')
    plt.show()


if __name__ == '__main__':
    run()
