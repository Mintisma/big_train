import jieba
import jieba.analyse
from CHlikelihood.likelihood import Likelihood

from utils.split_word import para2sent, sent2word

"""
得出最大tfidf列表
"""


def content4tfidf(content):
    """
    :param content: content of the news text, in str() format.
    :return: pre_processed content, in str() format.
    """
    new_content = ''
    sentences = para2sent(content)
    for sentence in sentences:
        words = sent2word(sentence)
        new_content += ' '.join(words)
    return new_content


def sentence_tfidf(content, topK=5):
    """
    调用content4tfidf, 因此不需要再使用set_stopwords,和set_tfidf_path函数了

    return: a string contents the main keywords in the content text
    """
    content = content4tfidf(content)
    result = jieba.analyse.extract_tags(content, topK=topK)
    text_essence = ' '.join(result)
    return text_essence


def level_likelihood(content, topK=5):
    """
    调用sentence_tfidf;
    余弦相似度计算中使用的分词方法为默认模式，不需要再定制（因为输入内容已经处理得很好了）

    return: a list of tuple, (likelyhood, sentences_index)
    """
    # 初始化余弦相似度计算器
    a = Likelihood()
    # 获取所有句子
    sentences = para2sent(content)
    # 获取文章主干
    text_essence = sentence_tfidf(content, topK=topK)
    # 计算并保存
    alike_lst = []
    i = 0
    for sentence in sentences:
        if sentence is not None:
            alike_value = a.likelihood(sentence, text_essence)
            if type(alike_value) is float:
                alike_lst.append((alike_value, i))  # 相似度, 文章中句子index
                i += 1
    result = sorted(alike_lst, reverse=True)
    return result