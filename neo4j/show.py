# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import math


def neo4j():
    providers = pd.read_csv("F:\\neo4jcsv\\3_12.csv")
    node = pd.DataFrame(providers)
    print(node.head(60))
    print(f'总节点数：{len(node)}')  # 总节点数：96,1309


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    neo4j()
