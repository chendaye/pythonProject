import pandas as pd
import csv
import re
import collections

# 替换引号
def replace(s):
    return re.sub("['\"]", "", s)

# 获取全部作者 文章标题关键字排序
def keywordOrder(input_path, ouput_path):
    input = pd.read_csv(input_path)
    output_csv_file = open(ouput_path, "a+", newline='')
    output_writer = csv.writer(output_csv_file)
    # keyword.csv scheme
    output_scheme = ("author_id", "author_name", "keywords")
    output_writer.writerow(output_scheme)
    exclude = ["was", "An", "a", "an", "never", "for", "of", "on", "in",
               "and", "A", "With", "the", "to", "It", "was", "by", "The", "On",
               "On", "that", "with", "at", "At", "(was", "published)",
               "Using","using", "Based", "based", "From", "from", "As", "as", "Does",
               "does", "Use", "use", "Toward", "toward", "All", "all"] # 无效字符
    for i in range(len(input)):
        # 处理排序
        author_id = input["author_id"][i];
        author_name = input["node"][i];
        articles = input["articles"][i].split("@") # list
        word_dict = collections.OrderedDict() #有序字典
        # 一个作者多篇文章
        for article in articles:
            info = article.split("#") # article_id#title#journal#year
            if len(info) >= 2:
                words = info[1].split() # 按空格拆分word
                # 一篇文章多个关键字
                for word in words:
                    if word not in exclude:
                        word = word.strip(":")
                        word = word.strip("\"")
                        if word in word_dict:
                            word_dict[word] += 1
                        else:
                            word_dict[word] = 1
        # 字典排序
        ans = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
        if len(ans) > 0:
            keyword = ""
            for oeder in ans:
                keyword = keyword + oeder[0]+"#"+str(oeder[1])+"@"
            print(keyword)
            output_writer.writerow((author_id, author_name, keyword.strip(",")))
    output_csv_file.close()




if __name__ == '__main__':
    input_path = "./data/csv/author_articles.csv"
    out_path = f"./data/csv/keyword.csv"
    keywordOrder(input_path, out_path)




