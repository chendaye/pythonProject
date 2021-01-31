import nltk
import pandas as pd
import csv
from nltk import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import re
import string

stopWords = []
dictionary = [] # 保存 dblp 中所有的 单词

# 替换引号
def replace(s):
    if isinstance(s, str) is not True:
        s = str(s)
    return re.sub("['\.\"\\\]", "", s)

# 判断变量类型的函数
def typeof(variate):
    type = None
    if isinstance(variate, int):
        type = "int"
    elif isinstance(variate, str):
        type = "str"
    elif isinstance(variate, float):
        type = "float"
    elif isinstance(variate, list):
        type = "list"
    elif isinstance(variate, tuple):
        type = "tuple"
    elif isinstance(variate, dict):
        type = "dict"
    elif isinstance(variate, set):
        type = "set"
    return type

 # 返回变量类型
def getType(variate):
    arr = {"int": "整数", "float": "浮点", "str": "字符串", "list": "列表", "tuple": "元组", "dict": "字典", "set": "集合"}
    vartype = typeof(variate)
    if not (vartype in arr):
        return "未知类型"
    return arr[vartype]

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


def isEmpty(string):
    val = str(string)
    return val if len(val) > 0 and val != "nan" else "--"

# 获取 paper-[]-author
def authorPaper(write, path):
    df = pd.read_csv(path)
    for i in range(len(df)):
        try:
            author_id = df["author_hash"][i]
            article = df["article"][i]
            paper = article.split("#")
            paper_id = paper[0]
            print(paper)
            write.writerow((author_id, paper_id))
        except IOError:
            print("IOError1>>>>"+df["article"][i])
        

# 获取 paper
def paperNode(write, path):
    df = pd.read_csv(path)
    for i in range(len(df)):
        try:
            # article_id,author,title,journal,year,ee,mdate,key,publtype,reviewid,rating
            article_id = df["article_id"][i]
            # author = replace(df["author"][i])
            title = replace(df["title"][i])
            journal = df["journal"][i]
            year = isEmpty(df["year"][i])
            ee = isEmpty(df["ee"][i])
            mdate = isEmpty(df["mdate"][i])
            key = isEmpty(df["key"][i])
            publtype = isEmpty(df["publtype"][i])
            reviewid = isEmpty(df["reviewid"][i])
            rating = isEmpty(df["rating"][i])

            print(article_id)
            write.writerow((article_id,title,journal,year,ee,mdate,key,publtype,reviewid,rating))
        except IOError:
            print("IOError1>>>>")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # # todo: author-[]-paper
    # author_path = "data/csv/paper_author.csv"
    # author_csv_file = open(author_path, "a+", newline='')
    # article_writer = csv.writer(author_csv_file)
    # article_scheme = ("author_id", "paper_id")
    # article_writer.writerow(article_scheme)
    # for i in range(100):
    #     path = f"./data/hash/author/author_{i}.csv"
    #     print(f"当前正在处理文件：{path}")
    #     authorPaper(article_writer, path)
    # author_csv_file.close()

    # todo: paper
    paper_path = "data/csv/paper.csv"
    paper_csv_file = open(paper_path, "a+", newline='')
    paper_writer = csv.writer(paper_csv_file)
    paper_scheme = ("paper_id","title","journal","year","ee","mdate","key","publtype","reviewid","rating")
    paper_writer.writerow(paper_scheme)
    path = f"data/csv/article.csv"
    paperNode(paper_writer, path)
    paper_csv_file.close()









