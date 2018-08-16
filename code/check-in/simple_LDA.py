# coding=utf-8
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora,models
import gensim
import numpy as np
'''
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."

doc_b = "My mother spends a lot of time driving my brother around to baseball practice."

doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."

doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."

doc_e = "Health professionals say that brocolli is good for your health."
'''

#划分数据，返回提取后的词干列表
def divide_data(s):

    tokenizer = RegexpTokenizer(r'\w+')  # 分词方式（也可以选择其他分词方式）

    en_stop = get_stop_words('en')  # 采用英语的停用词（例如for or）

    p_stemmer = PorterStemmer()  # 用于提取单词的词干（如“stemming”，“stemmer”，“stemmed”提取为stem，但不一定能够还原到正确的词干，但是能保证不同词词干的一致性）

    raw = s.lower()  # 将大写字母转换为小写

    tokens = tokenizer.tokenize(raw)  # 将每句话分成单词并存储在列表中

    stop_tokens = [i for i in tokens if i not in en_stop]  # 删除列表中的停用词

    stemmed = [p_stemmer.stem(i) for i in stop_tokens]  # 提取列表中每个词的词干

    return stemmed

def test_data():
    file = open('C:\\Users\\Client\\Desktop\\mycorpus.txt')
    doc_set = []
    for line in file:
        doc_set.append(line.strip())  # 将所有的数据存储到一个一维的list中

    print(doc_set)
    file.close()

    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

    texts = []  # 二维的列表，用于存储处理后的每句话的词干信息

    for i in doc_set:

        stemmed = divide_data(i)

        texts.append(stemmed)  # 将词干列表存储到二维列表中

    print(texts)

    dictionary = corpora.Dictionary(texts)  # Dictionary() 方法遍历所有的文本，为每个不重复的单词分配一个单独的整数 ID，同时收集该单词出现次数以及相关的统计信息。试试用 print(dictionary.token2id) 来查看每个单词的id。
    print(dictionary.token2id)
    print(dictionary.dfs)

    corpus = [dictionary.doc2bow(text) for text in texts]  # doc2bow() 方法将 dictionary 转化为一个词袋。得到的结果 corpus 是一个向量的列表，向量的个数就是文档数。在每个文档向量中都包含一系列元组
    print('corpus', corpus)

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)  # 生成的LDA模型

    print(ldamodel.print_topics(num_topics=3, num_words=2))
   # print(type(ldamodel))
    return dictionary,ldamodel

test_data()



'''
基于训练出的dictionary和ldamodel求新的文本的主题分布，方便比较两个文本之间相似性（因为测试集中所有的文本都是基于训练集的dictionary和ldamodel）
测试集中文本的主题数与训练集中LDA指定的主题数目一致
doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
doc_lda = lda[doc_bow]  # 得到新文档的主题分布
'''


dic = test_data()[0]
lda = test_data()[1]
s = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."

stemmed = divide_data(s)

print('stemmed',stemmed)

doc = dic.doc2bow(stemmed)

doc_lda = lda[doc]

print(doc_lda)#标号应该是主题号，与ldamodel中的主题号对应一致，概率是基于测试集的主题分布的概率分布，如(0, 0.03500115)对应着(0, '0.068*"mother" + 0.068*"brother"')表示在该测试文本中，mother，brother这个主题占的比重为0.03500115。3个主题的概率和为1,
list_doc1 = [i[1] for i in doc_lda]
print('list_doc1',list_doc1)


'''
try:
    sim = np.dot(list_doc1, list_doc2) / (np.linalg.norm(list_doc1) * np.linalg.norm(list_doc2))
except ValueError:
    sim=0
'''


