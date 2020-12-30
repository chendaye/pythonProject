import xml.sax
import csv
import os
from itertools import combinations


articleCsvPath = "../data/dblp/article.csv"
authorCsvPath = "../data/dblp/node.csv"
relationshipCsvPath = "../data/dblp/relationship.csv"

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
        # article_list
        self.article_list = []
        # node => author_id
        self.author_dict = dict()
        # node => ((title_id, title), (...))
        self.author_article_dict = dict()
        # relationship relation_flag => (start, weight, end)
        self.relationship_dict = dict()




    #todo: 元素开始调用.每一行都调用此方法
    def startElement(self, tag, attributes):
        self.CurrentTag = tag
        if tag == "article":
            # 标签属性
            self.mdate = attributes["mdate"] if "mdate" in attributes else ""
            self.key = attributes["key"] if "key" in attributes else ""
            self.publtype = attributes["publtype"] if "publtype" in attributes else ""
            self.reviewid = attributes["reviewid"] if "reviewid" in attributes else ""
            self.rating = attributes["rating"] if "rating" in attributes else ""
            self.rating = attributes["cdate"] if "cdate" in attributes else ""


        # 读取字符时调用

    def characters(self, content):
        if self.CurrentTag == "node":
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
            self.article_list.append((
                        self.article_id,
                        "|".join(self.author),
                        self.title,
                        self.journal,
                        self.year,
                        "|".join(self.ee),
                        self.mdate,
                        self.key,
                        self.publtype,
                        self.reviewid,
                        self.rating))
            # print(tag+"=="+str(self.article_id) +"===" +self.title)

            # node
            auId = []
            for p in self.author:
                # 节点 node 信息 id name article_list
                curArticle = (str(self.article_id), self.title, self.journal, self.year)
                if p in self.author_dict:
                    curp = self.author_dict.get(p)
                    auId.append(curp[0])
                    curp[2].append(curArticle) # 当前作者发表的文章 list
                else:
                    self.author_dict.update({p: (self.author_id, p, [curArticle])})
                    auId.append(self.author_id)
                    self.author_id += 1
            # relationship 作者超过 100 就只取前面 100个
            if len(auId) > 100:
                print(str(self.article_id) + ":count=" + str(len(auId)))
                print(auId)
                auId = auId[0:99]
            for p in list(combinations(auId, 2)):
                relationshipKey = str(p[0]) + "-" + str(p[1])
                if relationshipKey in self.relationship_dict:
                    rls = self.relationship_dict.get(relationshipKey)
                    rls[1] += 1  # 边的权重增加
                else:
                    self.relationship_dict.update({relationshipKey: [p[0], 1, p[1]]})  # 新增一条边

            # 重置xml数据
            self.resetArticle()
            self.article_id += 1
        self.CurrentTag = ""



    # 创建csv文件
    def writeCsvScheme(self, scheme, path):
        if not os.path.exists(path):
            with open(path, "a+", newline='') as file:
                csv_file = csv.writer(file)
                csv_file.writerow(scheme)


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
    # 解析xml
    # parser.parse("../data/dblp/test.xml")
    parser.parse("../data/dblp/temp/dblp.xml")

    # 创建 article.csv
    articleScheme = (
    "article_id", "node", "title", "journal", "year", "ee", "mdate", "key", "publtype", "reviewid", "rating")
    Handler.writeCsvScheme(articleScheme, articleCsvPath)
    with open(articleCsvPath, "a+", newline='') as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
        csv_file = csv.writer(file)
        for atl in Handler.article_list:
            csv_file.writerow(atl)

    # 创建author.csv
    authorScheme = ("author_id", "name", "article_list")
    Handler.writeCsvScheme(authorScheme, authorCsvPath)
    author_id = 0
    with open(authorCsvPath, "a+", newline='') as file:
        csv_file = csv.writer(file)
        for au in Handler.author_dict.values():
            strArticle = []
            for ar in au[2]:
                strArticle.append("#".join(ar))
            csv_file.writerow((au[0], au[1], "@".join(strArticle)))

    # 创建 relationship.csv
    relationshipScheme = ("start", "weight", "end")
    Handler.writeCsvScheme(relationshipScheme, relationshipCsvPath)
    with open(relationshipCsvPath, "a+", newline='') as file2:
        csv_file = csv.writer(file2)
        for rd in Handler.relationship_dict.values():
            csv_file.writerow((rd[0], rd[1], rd[2]))
