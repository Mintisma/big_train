import os
from datetime import datetime, timedelta

base_path = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(base_path, 'corpus')

stopwords_file = os.path.join(corpus_path, '新停用词包.txt')
cut_words_file = os.path.join(corpus_path, '财经词典.txt')

sentiment_words_file = os.path.join(corpus_path, '财经词情感得分.txt')
sentiment_level_file = os.path.join(corpus_path, '程度副词_得分.txt')
neg_words_file = os.path.join(corpus_path, '否定词.txt')

company_list = [
    'aoma',
    'haier',
    'jiuyang',
    'langdi',
    'suboer',
    'tianji',
    'zhongxin',
    'geli',
    'laoban',
    'TCL',
    'meidi',
    'changhong',
    'haixing',
]

# date_calc = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
date_calc = datetime.today().date()