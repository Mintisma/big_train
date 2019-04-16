from concurrent.futures import ProcessPoolExecutor, as_completed
import time

import pandas as pd

from settings import company_list, date_calc
from func4main import senti_day, score2level


def get_csv():
    result = []
    # for company in company_list:
    #     score = senti_day(company)
    #     result.append((date_calc ,company, score))

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(senti_day, (company)) for company in company_list]
        for future in as_completed(futures):
            company, score = future.result()
            result.append((date_calc ,company, score))

    df = pd.DataFrame(result, columns=('time', 'company', 'senti_score'))
    df.senti_score = df.senti_score.apply(score2level)
    df.to_csv('senti_score_{}.csv'.format(date_calc), index=False)


if __name__ == '__main__':
    start_time = time.time()
    get_csv()
    print('一共耗时{}秒'.format(time.time() - start_time))