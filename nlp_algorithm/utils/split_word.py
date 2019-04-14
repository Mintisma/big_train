from collections import defaultdict
import re

import jieba

from settings import stopwords_file, cut_words_file, sentiment_words_file, sentiment_level_file, neg_words_file


def readLines(text):
    """
    :param text: 一个文本文件
    :return: 文本文件产生的list
    """
    lst = []
    with open(text) as f:
        for line in f.readlines():
            line = line.replace('\n', '').replace('\t', '')
            lst.append(line)
    return lst


def para2sent(text):
    """
    :param text: 文章正文的任意一个段落
    :return: 该段落对应的句子构成的list, 根据目标进行编辑加工后
    """
    # 替换掉情感分析无关的文本内容：不相关词汇
    pattern = r'[、a-zA-Z0-9_.%（）-]+'
    text = re.sub(pattern, '', text)
    text = text.replace('\u3000', '').replace('\n', '')
    # 为分句做准备：变更标点
    text = text.replace('？', '。').replace('！', '。')
    # 去除文与文章意义无关系的内容：文末的说明
    if '责任编辑' in text:
        text = text.split('责任编辑')[0]
    elif '本文来自' in text:
        text = text.split('本文来自')[0]
    elif '文章关键词' in text:
        text = text.split('文章关键词')[0]
        # 分词
    sents = text.split('。')
    sents = [sent for sent in sents if len(sent) != 0 and '报记者' not in sent]
    return sents


def sent2word(sentence, cut_words_file=cut_words_file, stopwords_file=stopwords_file):
    """
    :param sentence: return of function para2sent
    :param cut_words_file: 分词用词典文件(路径)
    :param stopwords_file: 分词用停用词文件(路径)
    :return: 一个list，元素由该句子分词以及去除停用词过后的word构成
    """
    jieba.load_userdict(cut_words_file)
    segResult = jieba.lcut(sentence)
    stopwords = readLines(stopwords_file)
    newSent = []
    for word in segResult:
        if word in stopwords:
            continue
        else:
            newSent.append(word)
    return newSent


def ordered_word(lst):
    """
    :param lst: return of function sent2word
    :return: a dict, dict.keys = cutted keywords; dict.values = cutted keywords order
    """
    wordDict = defaultdict(int)
    for i in range(len(lst)):
        if wordDict[lst[i]] != 0:
            continue
        wordDict[lst[i]] = i
    return wordDict


def classifyWords(wordDict, senDoc=sentiment_words_file, negDoc=neg_words_file, levelDoc=sentiment_level_file):
    """
    :param wordDict: return from function orderd_word
    :param senDoc: sentiment documents, each line contains a word and its sentiment score
    :param negDoc: negtive sentiment documents, each line contains a negtive sentiment word
    :param levelDoc: sentiment level document, each line contains a word and its level
    :return: 3 dicts, senWord, notWord, degreeWord respctively, in which each dict's key is the keyword in its
            respective category, and its value is the word of key's index in wordDict

    """
    # (1) 情感词: dict
    senList = readLines(senDoc)
    senDict = defaultdict()
    for s in senList:
        try:
            senDict[s.split(' ')[0]] = s.split(' ')[1]
        except Exception as e:
            pass
    # (2) 否定词: list
    notList = readLines(negDoc)
    # (3) 程度副词: dict
    degreeList = readLines(levelDoc)
    degreeDict = defaultdict()
    for d in degreeList:
        try:
            degreeDict[d.split(',')[0]] = d.split(',')[1]
        except Exception as e:
            print('adverb Dict error: %s' % (e))

    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()

    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]  # 映射出（地址：senti得分）
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1  # 映射出（地址：否定）
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]  # 映射出（地址：程度）
    return senWord, notWord, degreeWord
