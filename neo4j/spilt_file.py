# -*- coding:utf-8 -*-
# author:chenpeng
# date: 2017-11-07
# 作用：根据需要拆分的文件数，拆分文件
# 备注：可以拆分csv格式文件和txt格式文件，返回的数据均是没有表头
import os
import pandas as pd


def file_split(filename, file_num):
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
        chunk.to_csv((f'F:\\neo4jcsv\\shared_members_mini_{i}.csv').format(head, i, tail), header=None, index=False)
        print(f'保存第{i}个数据'.format(i))
        i += 1



if __name__ == '__main__':
    filename = "F:\\neo4jcsv\\shared_members.csv"
    file_split(filename, 5)