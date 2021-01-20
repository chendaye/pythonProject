import os
import pandas as pd

def msg(path):
    df = pd.read_csv(path)
    print(f"总行数：{len(df)}")

def split(filename, file_num, save_path):
    # 获得每个文件需要有的行数
    chunksize = 1000000  # 先初始化的chunksize是100W
    data1 = pd.read_table(filename, chunksize=chunksize, sep=',', encoding='gbk')
    num = 0
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
    # 查分边
    relation_path100 = "./data/Graph/dblp100%_vertices.txt" # 992,5613
    relation_path20 = "./data/Graph/dblp20%_vertices.txt" # 39,3962
    split(relation_path100, 10, "./data/csv/relationship/relationship")
    # 拆分节点
    node_path = "./data/node.csv" # 210,1224
    split(node_path, 4, "data/csv/node/node")