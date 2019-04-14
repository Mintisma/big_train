import numpy as np
from utils.split_word import para2sent, sent2word, ordered_word, classifyWords


def scoreSent(senWord, notWord, degreeWord):
    """
    :param senWord: senWord from classifyWords. it is a dict().
    :param notWord: notWord from classifyWords. it is a dict().
    :param degreeWord: degreeWord from classifyWords. it is a dict().
    :return: sentiment score. it is an int().
    """
    score = 0
    # 存所有情感词的位置的列表
    senLoc = list(senWord.keys())
    notLoc = list(notWord.keys())
    degreeLoc = list(degreeWord.keys())
    senloc = -1

    # 遍历句中所有情感单词senWord，sent_score_word = sent_word * degree * not
    for i in senLoc:
        W = 1
        senloc += 1
        W *= float(senWord[i])

        for j in range(senLoc[senloc - 1], senLoc[senloc]):
            if j in notLoc:
                W *= -1
            if j in degreeLoc:
                if W < 0:
                    W *= float(degreeWord[j]) ** -1  # 程序词在否定意义上表示消弱程度，而非加强，因此取倒数
                else:
                    W *= float(degreeWord[j])

        # 调整权重, sent_score_sentence = sum(sent_score_word)
        score += W

        # i定位至下一个情感词
        i += 1
    return score


def title_senti_weight(senWord):
    senTitle = dict()
    for key in senWord.keys():
        value = float(senWord[key]) * 3
        senTitle[key] = value
    return senTitle


def calc_senti(title, text):
    # text score
    sents = para2sent(text)  # turn text into sentences
    lst = []
    for sent in sents:
        lst_word = sent2word(sent)  # turn each sentence into list of keywords
        dct_word = ordered_word(lst_word)  # turn each sentence into dict of keywords with value as index
        senWord, notWord, degreeWord = classifyWords(dct_word)
        lst.append(scoreSent(senWord, notWord, degreeWord))

    # title score
    lst_word = sent2word(title)
    dct_word = ordered_word(lst_word)
    senWord, notWord, degreeWord = classifyWords(dct_word)
    senTitle = title_senti_weight(senWord)
    lst.append(scoreSent(senTitle, notWord, degreeWord))
    return np.array(lst).mean()

