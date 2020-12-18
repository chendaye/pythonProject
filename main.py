# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd

def neo4j():
    providers = pd.read_csv("F:\\neo4jcsv\\providers.csv")
    df1 = pd.DataFrame(providers)
    # 保存前3w个节点
    node = df1.head(300)
    node.to_csv("F:\\neo4jcsv\\providers_mini.csv")

    node_dict = node.to_dict()
    node_list = []
    for key in node_dict['physicianId']:
        current = node_dict['physicianId'][key]
        node_list.append(current)
    # 排序
    node_list.sort()
    # 最大值 最小值
    min = node_list[0]
    max = node_list[len(node_list) - 1]
    # print(node_list)
    print(f'[{min}, {max}]')

    shared_members = pd.read_csv("F:\\neo4jcsv\\shared_members.csv")
    df2 = pd.DataFrame(shared_members)

    # 找到所有与选出来的节点想关联的边
    # df3 = df2[df2['startId'].isin(node_list) | df2['endId'].isin(node_list)]
    df3 = df2[df2['startId'].isin(node_list)]
    df4 = df2[df2['endId'].isin(node_list)]
    df3.append(df4)
    print(len(df3))
    # df3_dict = df3.to_dict()
    # print(df3_dict['startId'])
    # for key in df3_dict:
    #     for k in df3_dict[key]:
    #         print(df3_dict[key][k])
    #     break

    # df3 = df2.query(f'startId >= {min} & startId <= {max}  ')
    # df3.to_csv("F:\\neo4jcsv\\shared_members_mini.csv")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    neo4j()


