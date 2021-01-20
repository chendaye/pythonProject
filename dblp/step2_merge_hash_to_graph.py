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
    return re.sub("['\"\\\]", "", s)

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

# 全部的边
def articleRelationship(write, path):
    df = pd.read_csv(path)
    article_dict = dict()
    for i in range(len(df)):
        hash = df["relationship_hash"][i]
        start = df["start"][i]
        weight = df["weight"][i]
        end = df["end"][i]
        if start != end: # 不能自己指向自己
            if hash in article_dict.keys():
                article_dict[hash][1] += 1
            else:
                article_dict.update({hash: [start, weight, end]})
    for ar in article_dict.values():
        write.writerow((ar[0], ar[1], ar[2]))


# 重新整理 author_articles_tmp.csv
def removeQuote():
    author_path = "data/csv/author_articles.csv"
    author_csv_file = open(author_path, "a+", newline='')
    article_writer = csv.writer(author_csv_file)
    article_scheme = ("author_id", "node", "articles", "words")
    article_writer.writerow(article_scheme)
    for i in range(8):
        path = f"./data/csv/temp/node_{i}.csv"
        print(f"当前正在处理文件：{path}")
        df = pd.read_csv(path)
        for i in range(len(df)):
            author_id = df["author_id"][i]
            node = df["node"][i]
            article = replace(df["articles"][i]) # 去掉文章中的引号
            words = df["words"][i]
            article_writer.writerow((author_id, node, article, words))
    author_csv_file.close();

# 重新整理 author_articles_tmp.csv
def removeQuoteOnlyWord():
    author_path = "data/csv/author_articles.csv"
    author_csv_file = open(author_path, "a+", newline='')
    article_writer = csv.writer(author_csv_file)
    article_scheme = ("author_id", "node",  "words")
    article_writer.writerow(article_scheme)
    for i in range(8):
        path = f"./data/csv/node/node_{i}.csv"
        print(f"当前正在处理文件：{path}")
        df = pd.read_csv(path)
        for i in range(len(df)):
            author_id = df["author_id"][i]
            node = df["node"][i]
            words = df["words"][i]
            article_writer.writerow((author_id, node, words))
    author_csv_file.close();





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # str = '2533242816,Alex Gittens,"1437942#Tensor machines for learning target-specific polynomial features.#CoRR#2015@1582153#MALOnt: An Ontology for Malware Threat Intelligence.#CoRR#2020@158233#Sketched Ridge Regression: Optimization Perspective, Statistical Perspective, and Model Averaging.#J. Mach. Learn. Res.#2017@1361984#Alchemist: An Apache Spark MPI Interface.#CoRR#2018@1616276#Approximate Spectral Clustering via Randomized Sketching.#CoRR#2013@1558790#Improved matrix algorithms via the Subsampled Randomized Hadamard Transform#CoRR#2012@1578129#Accelerating Large-Scale Data Analysis by Offloading to High-Performance Computing Libraries using Alchemist.#CoRR#2018@1555216#Compact Random Feature Maps.#CoRR#2013@1350630#Fast Fixed Dimension L2-Subspace Embeddings of Arbitrary Accuracy, With Application to L1 and L2 Tasks.#CoRR#2019@2235439#Group Collaborative Representation for Image Set Classification.#Int. J. Comput. Vis.#2019@1639625#Revisiting the Nystrom Method for Improved Large-Scale Machine Learning#CoRR#2013@2440486#(was never published)##1993@1261062#Improved Matrix Algorithms via the Subsampled Randomized Hadamard Transform.#SIAM J. Matrix Anal. Appl.#2013@1577710#The spectral norm error of the naive Nystrom extension#CoRR#2011@158893#Scalable Kernel K-Means Clustering with Nystr\""om Approximation: Relative-Error Bounds.#J. Mach. Learn. Res.#2019@2440504#An interactive visualization framework for performance analysis.#EAI Endorsed Trans. Ubiquitous Environ.#2015@1514989#Sketched Ridge Regression: Optimization Perspective, Statistical Perspective, and Model Averaging.#CoRR#2017@1346322#Scalable Kernel K-Means Clustering with Nystrom Approximation: Relative-Error Bounds.#CoRR#2017@1475621#Matrix Factorization at Scale: a Comparison of Scientific Data Analytics in Spark and C+MPI Using Three Case Studies.#CoRR#2016@158608#Revisiting the Nystrom Method for Improved Large-scale Machine Learning.#J. Mach. Learn. Res.#2016@262604#Alchemist: An Apache Spark  MPI interface.#Concurr. Comput. Pract. Exp.#2019",4781:tensor:1@57:machines:1@367:learning:3@66639:targetspecific:1@685:polynomial:1@617:features:1@203950:malont:1@1173:ontology:1@3820:malware:1@3758:threat:1@677:intelligence:1@49034:sketched:2@4735:ridge:2@371:regression:2@668:optimization:2@1171:perspective:4@857:statistical:2@448:model:2@1302:averaging:2@187721:alchemist:3@4731:apache:2@4732:spark:3@1032:interface:2@4580:approximate:1@1428:spectral:2@159:clustering:3@820:randomized:3@3088:sketching:1@889:improved:4@660:matrix:3@821:algorithms:2@24032:subsampled:2@11529:hadamard:2@2238:transform:2@2890:accelerating:1@237:largescale:3@18:data:2@5:analysis:2@6593:offloading:1@95:highperformance:1@96:computing:1@3424:libraries:1@4306:compact:1@616:random:1@578:feature:1@4345:maps:1@467:fast:1@2291:fixed:1@2181:dimension:1@601:subspace:1@2698:embeddings:1@2701:arbitrary:1@923:accuracy:1@327:application:1@2491:tasks:1@445:group:1@2439:collaborative:1@622:representation:1@597:image:1@558:classification:1@2646:revisiting:2@55541:nystrom:5@664:method:2@366:machine:2@6:published:1@4068:norm:1@291:error:1@2112:naive:1@528:extension:1@481:scalable:2@550:kernel:2@702:kmeans:2@761:approximation:2@4744:relativeerror:2@1231:bounds:2@1:interactive:1@2:visualization:1@3:framework:1@4:performance:1@4830:factorization:1@271:scale:1@593:comparison:1@70:scientific:1@2389:analytics:1@187724:cmpi:1@796:three:1@1229:case:1@2663:studies:1'
    # print(replace(str))
    # removeQuoteOnlyWord()
    removeQuote()
    # # 要过滤的词
    # stopWords = stopWordsNltk()
    # # print(tokenizeNltk("Wissensbasierte` Wissensbasierte Wissensbasierte` Systeme: ] , { > in der Medizin: GMDS/GI, Abstracts\" des 1. gemeinsamen RENDEZVOUS Version 1: An Experimental English Language Query Formulation System for Casual Users of Relational Data Bases.#Research Report / RJ / IBM / San Jose, California 1990"))
    #
    # # todo: 作者&文章 写 author_articles_tmp.csv
    # author_path = "data/csv/author_articles_tmp.csv"
    # author_csv_file = open(author_path, "a+", newline='')
    # article_writer = csv.writer(author_csv_file)
    # article_scheme = ("author_id", "node", "articles", "words")
    # article_writer.writerow(article_scheme)
    # for i in range(100):
    #     path = f"./data/hash/author/author_{i}.csv"
    #     print(f"当前正在处理文件：{path}")
    #     authorNode(article_writer, path)
    # author_csv_file.close()
    #
    # #todo 字典
    # wordObject = open("./data/csv/word_map.txt", 'w')
    # inx = 0
    # for ip in dictionary:
    #     inx += 1
    #     wordObject.write(ip +"\t"+ str(inx))
    #     wordObject.write('\n')
    # wordObject.close()


    #
    # # todo: 边 写 relationships.csv
    # relation_path = "./data/csv/relationships.csv"
    # relation_csv_file = open(relation_path, "a+", newline='')
    # relation_writer = csv.writer(relation_csv_file)
    # relation_scheme = ("start", "weight", "end")
    # relation_writer.writerow(relation_scheme)
    # for i in range(100):
    #     path = f"./data/hash/relationship/relationship_{i}.csv"
    #     print(f"当前正在处理文件：{path}")
    #     articleRelationship(relation_writer, path)
    # relation_csv_file.close()




