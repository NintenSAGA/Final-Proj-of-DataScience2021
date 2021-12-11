import math
import pickle
import sys

import src

result_folder = src.__path__[0] + '/crawling/results/'
html_folder = result_folder + '~html/'
refined_text_folder = result_folder + '~refined_text/'

html_path = html_folder + '{}.html'
noise_path = result_folder + 'noise_set.pkl'
url_list = result_folder + '~url_list.txt'

noise_set = pickle.load(open(noise_path, 'rb'))
log = []

progress_bar = '\r[{}] {}'
pb_width = 50
pb_l_sign = '#'
pb_r_sign = '-'


def write(text: str):
    print(text, end='')


def update_progress_bar(progress: int, dest: int, anno: str):
    completed_ratio = float(progress + 1) / float(dest)
    completed_width = math.floor(pb_width * completed_ratio)
    write(progress_bar.format(pb_l_sign * completed_width + pb_r_sign * (pb_width - completed_width), anno))

