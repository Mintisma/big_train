import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

import pymysql
import numpy as np

from utils.main_text import main_text
from utils.calculate_sentiment import calc_senti


def get_data(company):
    """
    :param company: company name in database, e.g. 'aoma'.
    :param time: time precised to date, e.g. 2019-04-10.
    :return:
    """
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='*******77', db='big_train',
                               charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    sql = 'select title, content from sina_new WHERE company = "{company}" and type="news" and date<=CURRENT_DATE AND ' \
          'date>=(CURRENT_DATE -7) and LENGTH(content)>30'.format(company=company)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def senti_doc(result):
    """
    :param result: a tuple as (title, text) for a news.
    :return: sentiment score for that news
    """
    # get title and content text
    title = result[0]
    content = result[1]
    # get relevant content text
    main_content = main_text(content, topK=5)
    # calculate sentiment score
    senti = calc_senti(title, main_content)
    return senti


def senti_day(company):
    """
    :param company: company for sentiment evaluation
    :param time: date of interest
    :return: sentiment score for the company of the day specified
    """
    results = get_data(company)

    if len(results) == 0:
        result = (company, 0)
        return result

    scores = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(senti_doc, (result)) for result in results]
        for future in as_completed(futures):
            scores.append(future.result())

    score = int(np.array(scores).mean())
    result = (company, score)
    return result


def fix_scores(scores):
    result = []
    scores = list(scores)
    for score in scores:
        if type(score) is not int:
            score = 0
        result.append(score)
    return result


def score2level(result):
    if result < -18:
        level = 10
    elif result < -15:
        level = 9
    elif result < -12:
        level = 8
    elif result < -8:
        level = 7
    elif result < -5:
        level = 6
    elif result < -3:
        level = 5
    elif result < 0:
        level = 4
    elif result < 2:
        level = 3
    elif result < 5:
        level = 2
    elif result < 10:
        level = 1
    return level
