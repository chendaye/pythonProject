import csv
import pandas as pd



def readAttr():
    print("读入属性索引...")
    rt = pd.read_table("./data/Attribute/dblp_String2Int.txt", header=None)
    attr_list = []
    # 把属性映射放入 list
    for index, row in rt.iterrows():
        attr_list.append(row[0])
    print("属性索引读取完毕....")
    return attr_list


def writeGraph(in_path,out_path, attr_list):
    cnt = len(attr_list)
    # 写csv
    out_csv_file = open(out_path, "a+", newline='')
    out_writer = csv.writer(out_csv_file)
    out_scheme = ("author_id", "keywords") # 节点
    out_writer.writerow(out_scheme)
    # 读取 graph
    df = pd.read_table(in_path, header=None)
    for index, row in df.iterrows():
        print(row[0])
        print(row[1])
        int_attr = row[1].split(",")
        attr = []
        for ia in int_attr:
            name = attr_list[int(ia) - 1] if int(ia) < cnt else ""
            attr.append(str(ia) +":"+ str(name))
        out_writer.writerow((row[0], "#".join(attr)))
    out_csv_file.close()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    attr_list = readAttr()
    in_path = "./data/Attribute/dblp_attributes_int.txt"
    out_path = "./data/node.csv"
    writeGraph(in_path, out_path, attr_list)