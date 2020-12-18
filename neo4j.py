# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import math
import os

def getNode():
    base_path = "F:\\neo4jcsv"
    providers_path = "F:\\neo4jcsv\\providers.csv"
    shared_members_path = "F:\\neo4jcsv\\shared_members.csv"
    providers = pd.read_csv("F:\\neo4jcsv\\providers.csv")
    node = pd.DataFrame(providers)
    print(f'总节点数：{len(node)}')  # 总节点数：96,1309

def spiltRelationByReadTable():
    shared_members_path = "F:\\neo4jcsv\\shared_members.csv"
    step = 5000000
    num = math.ceil(34856900 / step)
    print(f'文件数：{num}')
    head, tail = os.path.splitext(shared_members_path)
    re = pd.read_table(shared_members_path, chunksize=step, sep=',', encoding='gbk')
    i = 0  # 定文件名
    for chunk in re:
        chunk.to_csv((f'F:\\neo4jcsv\\shared_members_mini_{i}.csv').format(head, 0, tail), index=False)
        print(f'保存文件：{i}')
        i += 1

    shared_members = pd.read_csv("F:\\neo4jcsv\\shared_members.csv")


def spiltRelationByReadCsv():
    step = 5000000
    num = math.ceil(34856900 / step)
    print(f'文件数：{num}')

    shared_members = pd.read_csv("F:\\neo4jcsv\\shared_members.csv")
    relation = pd.DataFrame(shared_members)

    print(f'总边数：{len(relation)}')  # 总边数：34,856900
    relation.head(1000000).to_csv("F:\\neo4jcsv\\shared_members_mini_1.csv")
    relation[48000000:31999999].to_csv(f'F:\\neo4jcsv\\test.csv')

    index = 0
    for x in range(num):
        x += 1
        start = index
        end = step * x - 1
        print(f'范围{x}：{start}~{end}')
        relation[start:end].to_csv(f'F:\\neo4jcsv\\shared_members_mini_{x}.csv')
        index += step * x

    #按行遍历 DataFrame
    for index, row in relation.head(10).iterrows():
        print(row)  # 输出每行的索引值



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    spiltRelationByReadTable()
