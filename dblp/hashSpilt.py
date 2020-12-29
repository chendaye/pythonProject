import xml.sax
import csv
import os
from itertools import combinations
import hashlib
import math


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
        # author => author_id
        self.author_dict = dict()
        # author => ((title_id, title), (...))
        self.author_article_dict = dict()
        # relationship relation_flag => (start, weight, end)
        self.relationship_dict = dict()

        self.hashCount = 100
        self.authorCount = 0
        self.relationCount = 0
        self.baseAuthorPath = "./data/hash/author"
        self.baseRelationshipPath = "./data/hash/relationship"
        self.authorHandleList = []
        self.authorWriteList = []
        self.relationshipHandleList = []
        self. relationshipWriteList = []




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
            #todo: 创建 article.csv 原始信息
            atl = (
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
                        self.rating)
            articleWriter.writerow(atl)

            #todo author
            auId = []
            inx = 0
            for p in self.author:
                # 节点 author 信息 id name article_list
                curArticle = (str(self.article_id),
                              self.title if self.title != "" else "",
                              self.journal if self.journal != "" else "",
                              self.year  if self.year != "" else "")
                print(curArticle)
                authorHashCode = self.getHashCode(p)
                # authorHashCode = self.article_id + inx
                authorHandleNo = self.convertToNumber(authorHashCode)
                try:
                    self.authorWriteList[authorHandleNo].writerow((authorHashCode, p, "#".join(curArticle))) # 保存一条文章
                except:
                    continue
                auId.append(authorHashCode)
                self.authorCount += 1
                inx += 1
                print(authorHandleNo)
                print("authorHash=>" + str(authorHashCode) + " 总计=" + str(self.authorCount))


            #todo: relationship 作者超过 100 就只取前面 100个
            if len(auId) > 100:
                auId = auId[0:99]
            inx = 0
            for p in list(combinations(auId, 2)):
                # relationshipHashCode = self.getHashCode(str(p[0]) + "-" + str(p[1]))
                relationshipHashCode = p[0]+ p[1] - 1  # 让 p[0] p[1] 确定一条边
                relationshipHandleNo = self.convertToNumber(relationshipHashCode)

                try:
                    self.relationshipWriteList[relationshipHandleNo].writerow((relationshipHashCode, p[0], 1, p[1]))
                except:
                    continue
                self.relationCount += 1
                inx += 1
                print(relationshipHandleNo)
                print(" relationshipHash=>" + str(relationshipHashCode) + " 总计=" + str(self.relationCount))


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

    def hashFile(self):

        for x in range(self.hashCount):
            # author 文件句柄
            author = self.baseAuthorPath+"/author_"+str(x)+".csv"
            authorCsvFile = open(author, "a+", newline='')
            authorWriter = csv.writer(authorCsvFile)
            authorScheme = ("author_hash", "name", "article")
            authorWriter.writerow(authorScheme)
            self.authorHandleList.append(authorCsvFile) # 打开的文件
            self.authorWriteList.append(authorWriter) # 写操作句柄

            # relationship 文件句柄
            relationship = self.baseRelationshipPath+"/relationship_"+str(x)+".csv"
            relationshipCsvFile = open(relationship, "a+", newline='')
            relationshipWriter = csv.writer(relationshipCsvFile)
            relationshipScheme = ("relationship_hash", "start", "weight", "end")
            relationshipWriter.writerow(relationshipScheme)
            self.relationshipHandleList.append(relationshipCsvFile)  # 打开的文件
            self.relationshipWriteList.append(relationshipWriter)  # 写操作句柄

    def hashFileClose(self):
        for handle in self.authorHandleList:
            handle.close()
        for handle in self.relationshipHandleList:
            handle.close()

    # 字符串转化为 整数
    def convertToNumber(self, hash):
        return hash % self.hashCount

    def getHashCode(self, s):
        hash = int.from_bytes(s.encode(), 'little')
        return hash

    def convertFromNumber(self, n):
        return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()



if (__name__ == "__main__"):

    #todo: 创建 article.csv
    articleCsvPath = "./data/csv/article.csv"
    articleCsvFile = open(articleCsvPath, "a+", newline='')
    articleWriter = csv.writer(articleCsvFile)
    articleScheme = (
    "article_id", "author", "title", "journal", "year", "ee", "mdate", "key", "publtype", "reviewid", "rating")
    articleWriter.writerow(articleScheme)

    #todo: 解析xml
    # 重写 ContextHandler
    Handler = dblpArticleHandler()
    Handler.hashFile() # 创建文件
    # 创建 XMLReader
    parser = xml.sax.make_parser()
    # 关闭命名空间
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(Handler)
    parser.parse("./data/dblp.xml")

    Handler.hashFileClose()
    #todo: 关闭文件
    articleCsvFile.close()


