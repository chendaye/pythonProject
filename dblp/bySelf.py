import xml.sax
import csv
import re
import time
import os

articleCsvPath = "../data/dblp/article.csv"
authorCsvPath = "../data/dblp/author.csv"

class dblpArticleHandler(xml.sax.ContentHandler):
    def __init__(self):
        # article
        self.author = []
        self.title = ""
        self.journal = ""
        self.year = ""
        self.ee = []
        self.mdate = ""
        self.key = ""
        self.publtype = ""
        self.reviewid = ""
        self.rating = ""
        self.cdate = ""
        # csv
        self.articleCsvPath = "../data/dblp/article.csv"
        self.author_set = set()

        # article_id
        self.article_id = 0
        # author_id
        self.author_id = 0
        # author => author_id
        self.author_dict = dict()
        # author => ((title_id, title), (...))
        self.author_article_dict = dict()
        # relationship relation_flag => (start, weight, end)
        self.relationship_dict = dict()




    #todo: 元素开始调用.每一行都调用此方法
    def startElement(self, tag, attributes):
        self.CurrentTag = tag
        if tag == "article":
            # 标签属性
            self.mdate = attributes["mdate"]
            self.key = attributes["key"]
            self.publtype = attributes["publtype"]
            self.reviewid = attributes["reviewid"] if "reviewid" in attributes else ""
            self.rating = attributes["rating"] if "rating" in attributes else ""
            self.rating = attributes["cdate"] if "cdate" in attributes else ""


        # 读取字符时调用

    def characters(self, content):
        if self.CurrentTag == "author":
            self.author.append(content)
        elif self.CurrentTag == "title":
            self.title = content
        elif self.CurrentTag == "journal":
            self.journal = content
        elif self.CurrentTag == "year":
            self.year = content
        elif self.CurrentTag == "ee":
            self.ee.append(content)


    #todo: 元素结束调用, 遇到头标签之后，再一行一行读取
    def endElement(self, tag):

        if tag == "article":
            # 创建 article.csv 原始信息
            self.saveAsCsv(articleCsvPath)

            # author-relationship
            i = 0
            for p in self.author:
                # 节点 author 信息 id name article_list
                curArticle = (self.article_id, self.title, self.journal, self.year)
                if p in self.author_dict:
                    curp = self.author_dict.get(p)
                    curp[2].append(curArticle) # 当前作者发表的文章 list
                else:
                    self.author_dict.update({p: (self.author_id, p, [curArticle])})
                    self.author_id += 1
                # relationship
                firstAuthorId = self.author_dict.get(self.author[0])[0]
                curAuthorId = self.author_dict.get(p)[0]
                if i > 0:
                    relationshipKey = str(firstAuthorId) +"-"+ str(curAuthorId) if firstAuthorId < curAuthorId else str(curAuthorId) +"-"+ str(firstAuthorId)
                    print(str(firstAuthorId)+"<>"+str(curAuthorId)+"<>"+relationshipKey)
                    if relationshipKey in self.relationship_dict:
                        rls = self.relationship_dict.get(relationshipKey)
                        rls[1] += 1 # 边的权重增加
                    else:
                        self.relationship_dict.update({relationshipKey: [firstAuthorId, 1, curAuthorId]}) # 新增一条边
                i += 1


            # 重置xml数据
            self.resetArticle()
        self.CurrentTag = ""
        self.article_id += 1



    def saveAsCsv(self, path):
        data = (self.article_id, "|".join(self.author), self.title, self.journal, self.year, "|".join(self.ee), self.mdate,
        self.key, self.publtype, self.reviewid, self.rating)

        with open(path, "a+", newline='') as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
            csv_file = csv.writer(file)
            csv_file.writerow(data)

    # 创建csv文件
    def writeCsvScheme(self, scheme, path):
        if not os.path.exists(path):
            with open(path, "a+", newline='') as file:
                csv_file = csv.writer(file)
                csv_file.writerow(scheme)


    def buildGraph(self):
        print(self.article_id)

    def resetArticle(self):
        self.author = []
        self.title = ""
        self.journal = ""
        self.year = ""
        self.ee = []
        self.mdate = ""
        self.key = ""
        self.publtype = ""
        self.reviewid = ""
        self.rating = ""
        self.rating = ""





if (__name__ == "__main__"):
    # 创建 XMLReader
    parser = xml.sax.make_parser()
    # 关闭命名空间
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # 重写 ContextHandler
    Handler = dblpArticleHandler()
    parser.setContentHandler(Handler)

    # 创建csv
    articleScheme = ("article_id", "author", "title", "journal", "year", "ee", "mdate", "key", "publtype", "reviewid", "rating")
    Handler.writeCsvScheme(articleScheme, articleCsvPath)

    # 解析xml
    parser.parse("../data/dblp/test.xml")

    # 创建author.csv
    authorScheme = ("author_id", "name")
    Handler.writeCsvScheme(authorScheme, authorCsvPath)
    author_id = 0
    with open(authorCsvPath, "a+", newline='') as file:
        csv_file = csv.writer(file)
        for author in Handler.author_set:
            csv_file.writerow((author_id, author))
            author_id += 1
    print(Handler.author_dict)
    print(Handler.relationship_dict)
