from src.crawling.common import refined_text_folder
from src.analysis.util.parser import parse_ch_num, parse_alcohol, parse_penalty
from src.analysis import util, json_folder
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
from scipy.stats import t
import math

json_list = util.json_reader(json_folder + '2021')


def parse_numeric_info():
    accu_freq_dict = {}
    res_list = []

    for j in json_list:
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
        res_list.append(j)
    return res_list


def run():
    res_list = parse_numeric_info()
    df = pd.DataFrame(res_list)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # df = df.loc[:, ['省份', '主刑', '附加刑', '酒精含量', '案件索引']]
    df = df[df['酒精含量'] >= 80]
    df = df[df['酒精含量'] <= 300]
    df = df[df['主刑'] <= 200]
    df = df[df['主刑'] >= 30]
    df = df[df['附加刑'] >= 1000]
    df = df[df['附加刑'] < 22000]
    df_all = df
    # df = df[df['省份'] == '广东省']  # type: pd.DataFrame
    # df = df.reset_index(drop=True)
    data = []
    for prov in "山东省 广东省 湖南省".split():
        data.append(prov_check(df, prov))
    print(util.table_generator('省份 rho1 p-value1 rho2 p-value2'.split(), data))

    # show_overview(df, df_all)


def prov_check(df: pd.DataFrame, prov: str) -> list:
    """
    分省份测试
    返回列表，包含：
    省份 rho1 p-value1 rho2 p-value2
    :param df:
    :param prov:
    :return:
    """
    def t_test(r, n):
        return r * math.sqrt(float(n - 2) / (1 - math.pow(r, 2)))
    ret = [prov]
    df = df[df['省份'] == prov]
    df = df.reset_index(drop=True)
    x = df['酒精含量']
    y1 = df['附加刑']
    y2 = df['主刑']
    nn = x.__len__()
    for y in (y1, y2):
        rho = x.corr(y)
        tt = t_test(rho, nn)
        p_value = t.cdf(tt, nn - 2)
        ret += ["%.4f" % rho, "%.4f" % p_value]
    return ret


def show_overview(df, df_all):
    # Get Unique continents
    color_labels = df_all['省份'].unique()
    # List of colors in the color palettes
    rgb_values = sns.color_palette("Set2", len(df_all['省份']))
    # Map continents to the colors
    color_map = dict(zip(color_labels, rgb_values))
    plt.rcParams["font.family"] = "Hei"
    for func in [lambda: sns.scatterplot(data=df, x='酒精含量', y='附加刑'),
                 lambda: sns.scatterplot(data=df, x='酒精含量', y='主刑')]:
        paint_graph(func)
    alc = df.get('酒精含量')
    a2d = df.loc[:, ['主刑', '附加刑']]
    a1d = do_pca(a2d)

    # scatter_draw(alc, a1d)


def paint_graph(func):
    func()
    plt.show()


def scatter_draw(a1, a2):
    fig, ax = plt.subplots()
    plt.rcParams["font.family"] = "Hei"
    ax.scatter(a1, a2)
    ax.set_xlabel('酒精含量')
    ax.set_ylabel('主刑与附加刑的线性组合')


def do_pca(array):
    r = array.sum()[1] / array.sum()[0]
    array = array.dot(np.array([[1, 0], [0, 1 / r]]))
    pca = PCA(1)
    pca.fit(array)
    return pca.transform(array)


if __name__ == '__main__':
    run()
