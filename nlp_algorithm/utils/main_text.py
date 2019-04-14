from utils.split_word import para2sent
from utils.tfidf_text import level_likelihood


def content_text(sentences, like_result):
    """
    :param sentences: a list of sentence, sentence is str()
    :param like_result:
    :return:
    """
    text_len = int(len(sentences) * 0.3) - 2
    s = ''
    for i in range(text_len):
        sentence_index = like_result[i][1]
        s += sentences[sentence_index]
    return s


def main_text(content, topK=5):
    """
    调用 content_text
    :param content: content of the news text
    :return: text relevant to the theme according to tfidf algorithm
    """
    if content is None:
        return ''
    sentences = para2sent(content)
    like_result = level_likelihood(content, topK=topK)
    if len(sentences) < 4:
        text = ''.join(sentences)
    elif len(sentences) < 10:
        text = sentences[0] + sentences[like_result[0][1]] + sentences[like_result[1][1]]
    else:
        text = content_text(sentences, like_result)
    return text