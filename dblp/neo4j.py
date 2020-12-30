import pandas as pd
import csv
import re

# 替换引号
def replace(s):
    return re.sub("['\"]", "", s)

# 获取全部作者及其文章（节点和属性）
def authorNode(write, path):
    df = pd.read_csv(path)
    author_dict = dict()
    for i in range(len(df)):
        hash = df["author_hash"][i]
        name = df["name"][i]
        article = replace(df["article"][i]) # 去掉文章中的引号
        if hash in author_dict.keys():
            author_dict[hash][2].add(article)
        else:
            author_dict.update({hash: [hash, name, {article}]})
    for au in author_dict.values():
        write.writerow((au[0], au[1], "@".join(au[2])))

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



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 作者&文章
    author_path = "./data/csv/author_articles.csv"
    author_csv_file = open(author_path, "a+", newline='')
    article_writer = csv.writer(author_csv_file)
    article_scheme = ("author_id", "node", "articles")
    article_writer.writerow(article_scheme)
    for i in range(100):
        path = f"./data/hash/author/author_{i}.csv"
        print(f"当前正在处理文件：{path}")
        authorNode(article_writer, path)
    author_csv_file.close()

    # 边
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


