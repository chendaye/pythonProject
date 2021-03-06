#!/usr/bin/python3
import nltk
import pandas as pd
import csv
from nltk import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import re
import string

stopWords = []
dictionary = [] # 保存 dblp 中所有的 单词


def stopWordsNltk():
    exclude = ["was",  "a", "an", "never", "for", "of", "on", "in",
               "and",   "the", "to", "it", "was", "by", "the",
               "On", "that", "with", "at", "using",  "based",  "from",  "as",
               "does", "use",  "toward", "all", ".", ":", ","]  # 无效字符

    stopWords = set(stopwords.words('english'))
    for exc in exclude:
        stopWords.add(exc)
    return stopWords

"""
用nltk 分词
"""
def tokenizeNltk(word):
    # 转小写
    word = word.lower()
    # 去除标点
    remove = str.maketrans('', '', string.punctuation)
    word = word.translate(remove)
    # 分词
    tokenizer = RegexpTokenizer(r'[a-z]{4,}') # 正则过滤 保留字母个数>=4的单词
    words = tokenizer.tokenize(word)
    # words = word_tokenize(word)
    # 去除停用词
    words = [word for word in words if word.lower() not in stopWords]
    freq_dist = nltk.FreqDist(words)
    return freq_dist

# 获取全部作者及其文章（节点和属性）
def authorNode(write, path):
    global dictionary_count
    df = pd.read_csv(path)
    author_dict = dict()
    for i in range(len(df)):
        hash = df["author_hash"][i]
        name = df["name"][i]
        article = df["article"][i]
        #article = replace(df["article"][i]) # 去掉文章中的引号
        if hash in author_dict.keys():
            author_dict[hash][2].add(article)
        else:
            author_dict.update({hash: [hash, name, {article}]})
    # dict 每一项都包含 作者hash 作者name 作者所有文章
    for au in author_dict.values():
        titles = []
        # 取出所有 title
        for wz in au[2]: # article_id#title#journal#year
            titles.append(wz.split("#")[1])
            # 分词
            words = tokenizeNltk(" ".join(titles))
            freq = []
            # 当前作者的词频信息
            for k,v in words.items():
                # 把词加入全局大词典中
                if k not in dictionary:
                    dictionary.append(k)
                # 当前作者的词频信息 词的索引:词:词频
                word = [str(dictionary.index(k) + 1), k, str(v)]
                word = ":".join(word)
                print(word)
                freq.append(word)
        write.writerow((au[0], au[1], "@".join(au[2]), "@".join(freq)))


 # 要过滤的词
stopWords = stopWordsNltk()
#print(tokenizeNltk("Wissensbasierte` Wissensbasierte Wissensbasierte` Systeme: ] , { > in der Medizin: GMDS/GI, Abstracts\" des 1. gemeinsamen RENDEZVOUS Version 1: An Experimental English Language Query Formulation System for Casual Users of Relational Data Bases.#Research Report / RJ / IBM / San Jose, California 1990"))

# todo: 作者&文章 写 author_articles_tmp.csv
author_path = "./author_articles_tmp.csv"
author_csv_file = open(author_path, "a+", newline='')
article_writer = csv.writer(author_csv_file)
article_scheme = ("author_id", "node", "articles", "words")
article_writer.writerow(article_scheme)
for i in range(100):
    path = "./author/author_"+str(i)+".csv"
    print("当前正在处理文件："+path)
    authorNode(article_writer, path)
author_csv_file.close()

#todo 字典
wordObject = open("./word_map.txt", 'w')
inx = 0
for ip in dictionary:
    inx += 1
    wordObject.write(ip +"\t"+ str(inx))
    wordObject.write('\n')
wordObject.close()