import pickle

import src

result_folder = src.__path__[0] + '/crawling/results/'
log = []
html_folder = result_folder + '~html/'
html_path = html_folder + '{}.html'
refined_text_path = result_folder + '~refined_text/'
noise_set = pickle.load(open(result_folder + 'noise_set.pkl', 'rb'))