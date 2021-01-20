import os
import pandas as pd

def msg(path):
    df = pd.read_csv(path)
    print(f"总行数：{len(df)}")

def split(filename, file_num, save_path):
    # 获得每个文件需要有的行数
    chunksize = 100000  # 先初始化的chunksize是100W
    data1 = pd.read_table(filename, chunksize=chunksize, sep=',', encoding='gbk')
    num = 0 # 文件总的行数
    for chunk in data1:
        num += len(chunk)
    chunksize = round(num / file_num + 1)

    # 需要存的file
    head, tail = os.path.splitext(filename)
    data2 = pd.read_table(filename, chunksize=chunksize, sep=',', encoding='gbk')
    i = 0  # 定文件名
    for chunk in data2:
        cur_path = f'{save_path}_{i}.csv'
        print(f"正在处理文件：{cur_path}")
        # chunk.to_csv(cur_path.format(head, i, tail), header=None, index=False)
        chunk.to_csv(cur_path.format(head, i, tail),  index=False)
        i += 1



"""
拆分整个图为，若干小文件
"""
if __name__ == '__main__':
    # 拆分 author_articles_tmp.csv words文件
    node_path = "data/csv/author_articles_tmp.csv"  # 271,8656
    # split(node_path, 8, "data/csv/temp/node")

    # 查分边
    relation_path = "./data/csv/relationships.csv" # 831,9365
    split(relation_path, 10, "./data/csv/relationship/relationship")
    # 拆分节点
    node_path = "data/csv/author_articles.csv"  # 271,8656
    # split(node_path, 8, "data/csv/node/node")


