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


 # 要过滤的词
stopWords = stopWordsNltk()
words = tokenizeNltk("Wissensbasierte` Wissensbasierte Wissensbasierte` Systeme: ] , { > in der Medizin: GMDS/GI, Abstracts\" des 1. gemeinsamen RENDEZVOUS Version 1: An Experimental English Language Query Formulation System for Casual Users of Relational Data Bases.#Research Report / RJ / IBM / San Jose, California 1990")
for k,v in words.items():
    print(k+":"+str(k))