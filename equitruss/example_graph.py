import csv
import pandas as pd

def writeNode(in_path,out_path):
    # 写csv
    out_txt_file = open(out_path, "a+", newline='')
    # 读取 graph
    df = pd.read_table(in_path, header=None)
    exclude = [304565,946299,1647914,1883367] # 测试社区
    for index, row in df.iterrows():
        if int(row[0]) in exclude:
            out_txt_file.write(f"{row[0]}\t{row[1]}\n")
    out_txt_file.close()

def writeRelationship(in_path,out_path):
    # 写csv
    out_txt_file = open(out_path, "a+", newline='')
    # 读取 graph
    df = pd.read_table(in_path, header=None)
    exclude = [304565,946299,1647914,1883367] # 测试社区
    for index, row in df.iterrows():
        if int(row[0]) in exclude or int(row[1]) in exclude:
            out_txt_file.write(f"{row[0]}\t{row[1]}\n")
    out_txt_file.close()

def writeRelationship2(in_path,out_path):
    exclude = [] # 测试社区
    ex = pd.read_table("./data/algo_relationship.csv")
    for index,row in ex.iterrows():
        if(int(row[0]) not in exclude):
            exclude.append(row[0])
        if(int(row[1]) not in exclude):
            exclude.append(row[1])
    # 写csv
    out_txt_file = open(out_path, "a+", newline='')
    # 读取 graph
    df = pd.read_table(in_path, header=None)

    for index, row in df.iterrows():
        if int(row[0]) in exclude:
            out_txt_file.write(f"{row[0]}\t{row[1]}\n")
    out_txt_file.close()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # in_path = "./data/Attribute/dblp_attributes_int.txt"
    # out_path = "./data/algo_node.csv"
    # writeNode(in_path, out_path)
    #
    # in_path = "./data/Graph/dblp20%_vertices.txt"
    # out_path = "./data/algo_relationship.csv"
    # writeRelationship(in_path, out_path)

    in_path = "./data/Attribute/dblp_attributes_int.txt"
    out_path = "./data/algo_node.csv"
    writeRelationship2(in_path, out_path)