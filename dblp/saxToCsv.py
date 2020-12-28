from xml.sax import handler, make_parser
import json
import re
import time
import os


# 所有作者信息都在以这些根标签内部
paper_tag  =['article','inproceedings','proceedings','book',
                    'incollection','phdthesis','mastersthesis','www']
'''
    选择的期刊或者会议
    包括CHI，VAST, TVCG, PacificVis， InfoVis，EuroVis，Information Visualization（期刊）,JOV(journal of visuzalition), The Visual Computer
'''

CHOOSE_VENUES = ['conf/chi/','conf/ieeevast/','journals/tvcg/','conf/apvis/','conf/infovis/','conf/vissym/','journals/cgf/','journals/ivs/','conf/jvis/','journals/vc/']


class xmlHandler(handler.ContentHandler):
    def __init__(self, parse_result_path, spe_chara_path, choose_venues, time):
        self.topTag = ""
        self.CurrentTag = ""
        self.key = ""
        self.authors = []       # 当前文章的作者
        self.currentYear = ""   # 当前文章出版时间
        self.extentYear = []    # 时间跨度范围
        self._filter_year = time    # 只取发表时间大于该时间的文章
        self.venue = ""             # 发表期刊或会议
        self.parse_result = []      # 解析记录，包括1.年份 2.作者 3.发表期刊或会议
        self.isExsitAuthor = {}     # 统计作者数量



    def startDocument(self):
        print('Start Parsing......')

    def endDocument(self):


        print(self.parse_result)

        self.extentYear.sort()

        print('Parse Successfully!')

    def startElement(self, tag, attrs):

        self.CurrentTag = tag # 当前标签类型

        #　记录下顶级标签类型，帮助在标签结束事件中判断一篇文章是否结束
        if tag in paper_tag:
            self.topTag = tag
            self.key = attrs["key"]

    def endElement(self, tag):
        # 判断是否类似article的跟标签结束并且发表时间在1988年之后，若结束，则将数据存进模型中
        if tag == self.topTag :
            authors = self.authors
            year = self.currentYear

            # 修正姓名
            for (i, name) in enumerate(authors):
                authors[i] = self.exchangeName(name)
            # record = [year, authors, venue], 一条记录包括 1.时间 2.作者 3.期刊或者会议名称
            record = [year, ";".join(authors).strip()]
            # 统计作者数量
            for a in record[1].split(";"):
                if a not in self.isExsitAuthor:
                    self.isExsitAuthor[a] = 1

            self.parse_result.append(record)
            # 当一篇文章结束，重新初始化
            self.topTag = ""
            self.CurrentTag = ""
            self.authors = []
            self.currentYear = ""
            self.key = ""
            self.venue = ""

    #　获取标签中的内容
    def characters(self, chrs):
        tag = self.CurrentTag
        if chrs.strip()!="":
            if tag == "author":
                self.authors.append(chrs.strip())
            elif tag == "year":
                self.currentYear = int(chrs)
                if (self.currentYear not in self.extentYear) and (self.currentYear>=self._filter_year):
                    self.extentYear.append(self.currentYear)


    # 拥有特殊字符的名字替换
    def exchangeName(self,name):
        matchStrs = re.findall(r',.{4,9};',name)
        for s in matchStrs:
            if s in self.specialC:
                name = name.replace(s,self.specialC[s])
        return name


def parse(source_file_path, parse_result_path, spe_chara_path, filter_venues, filter_time):
    if os.path.exists(source_file_path):
        handler = xmlHandler(parse_result_path, spe_chara_path, filter_venues,filter_time)
        parser = make_parser()
        parser.setContentHandler(handler)
        with open(source_file_path,'r') as fs:
            parser.parse(fs)
    else:
        print("需要解析的文件不存在或路径错误")

if __name__ == "__main__":
    source_file_path = "../data/dblp/test.xml"
    parse_result_path = "../data/dblp/parse_result.json"
    spe_chara_path = "../data/dblp/specialCharacter.json"


    start = time.time() # 开始时间
    parse(source_file_path,parse_result_path,spe_chara_path,CHOOSE_VENUES,1990)      # 解析xml
    end = time.time()  # 结束时间
    print("运行时间为：",end-start)