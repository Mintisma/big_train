# TDU_大实训作业  
实现按天生成一张csv表格，表格包含3列，分别是日期，公司名称，风险指数。风险指数按1-10（10分最危险）。

# 引用第三方库  
scrapy, jieba, pymysql, numpy, pandas, CHlikelihood

# 主要功能  
1. 每天爬取sina.com.cn中指定公司集的新闻数据，数据包含：公司名，爬取日期，新闻标题，新闻正文，新闻类别，新闻url
2. 每天生成一份csv表格，表格包含3列，分别是日期，公司名称，风险指数。风险指数按1-10（10分最危险）。

# 使用方法
使用crontab激活run_algorithm.sh，run_scrapy.sh这2个文件

# 代码结构
1. big_train/big_train: 包含了scrapy爬虫  
其它的说明:  
    * 数据库使用了mysql，pipeline中使用了异步插入。
    * 反爬虫设置DOWNLOAD_DELAY = 0.05。middlewares中设置了随机的user-agent（虽然目前sina还没有屏蔽user_agent, 可以说对爬虫非常友好）。
  
2. big_train/nlp_algorithm: 自然语言处理的算法
    * corpus文件夹包含分词与计算情感得分需要使用的词典  
    * main.py调用fun4main.py，生成最终需要的csv文件  
    * fun4main.py调用utils里的文件  
    * utils里存放计算方法
  
# 计算思路与实现路径  
1. 计算思路  
    * 新闻的情感 = 标题情感 + 正文情感  
    * 段落情感 = sum(句子情感)  
    * 句子情感 = sum(句中各个情感段)  
    * 情感段 = sentiment_calculation(否定词 + 程度词 + 情感词), sentiment_calculation是一个情感计算公式  
2. 数据预处理思路 
    * 文本中的数据并不是所有都有用，因此我们要做一些数据清理，将数字和情感无关的词汇去除。  
    * text中的句子并不是都能反映文章的主题，当text中的句子数量众多时，需要进行筛选。具体的，通过tfidf计算出text的主要词汇，然后
    逐句进行余弦相似度的对比。只将余弦相似度最高的若干句子放入情感计算的模型。  
    * 新闻包含title和text2个部分。通常title的作用会大于text。因此将title和text分别处理。  
3. corpus文档准备
    * 分词词典：财经词典.txt。本文档参考自[github](https://github.com/fighting41love/funNLP), 根据采集的文本的需要，做了词集的扩充。主要是现在的新闻当中网络用语提升，需要增加暴雷等词汇。
    * 情感得分词典：财经词情感得分.txt。文档参考自[github](https://github.com/ryanyuansufe/finsen)，扩充了一定的词汇量。并对负向情感评-2分，正向为1分。
    * 否定词词典：否定词.txt。参考自[github](https://github.com/fighting41love/funNLP)
    * 程度词词典：程序副词_得分.txt。 参考自[github](https://github.com/fighting41love/funNLP)，自定义程度得分自定义为0.5分-3分。
    * 停用词：新停用词.txt。参考自[github](https://github.com/fighting41love/funNLP)
2. 实现  
    1. 数据预处理。除了删除停用词外，还会将新闻文本中最后的责任编辑等段落进行清洗。
    2. 分词，数据结构上str变为list。这里利用了jieba.user_dict('财经词典')，增加分词的准确率
    3. 根据分词结果建立词汇与词汇在文本中所在的位置的字典。dict_file = {keyword: keyword_index}。
    4. 建立dict_senti={keyword_index: 情感得分}, dict_level={keyword_index: 程度得分}，list_neg=[否定词_index]  
    前4个小点的功能由`utils/split_word.py`实现  
    5. 计算情感得分。根据计算思路，我们利用dict_senti中的keyword_index找到每个情感词对应在文章中的位置。这样就可以把文本当作由若干个情感词集组成的了。
      然后，每个词集当中，如果还存在程度词和反转词，我们再分别进行情感的加权。  
    第5个小点的功能由`utils/calculate_sentiment.py`实现  
    6. text中的核心句提取。核心句提取分2步，首先利用tfidf算法求出当前文本中最重要的topK个关键词(默认为5)，这里tfidf中的docoment frequency使用的是
      jieba默认的文本；然后依次计算所有句子与这topK个关键词的余弦相似度，存入一个list内按相似度降序排列。完成第1步后，再根据文本中句子的总数量，提取
      需要的句子。根据经验，新闻的正文的第一句话总是需要的。  
      以上功能分别由`utils/tfidf_text.py`和`utils/main_text.py`完成  
    7. 从数据库中调出**某公司**在最近7天的所有新闻的标题和正文，计算所有文章的平均情感得分作为该公司当天的风险得分。  
      第7点功能由`func4main.py`实现  
    8. 计算所有感兴趣公司的风险得分，并将结果导出成csv文件。  
      第8点功能由`main.py`实现
      
  
  

   
  

