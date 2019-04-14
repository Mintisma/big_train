import pandas as pd

from settings import company_list, date_calc
from func4main import senti_day, score2level


def get_csv():
    result = []
    for company in company_list:
        score = senti_day(company)
        result.append((date_calc ,company, score))

    df = pd.DataFrame(result, columns=('time', 'company', 'senti_score'))
    df.senti_score = df.senti_score.apply(score2level)
    df.to_csv('senti_score_{}.csv'.format(date_calc), index=False)


if __name__ == '__main__':
    get_csv()