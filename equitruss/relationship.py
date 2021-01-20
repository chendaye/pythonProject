import csv
import pandas as pd



def readRelationship():
    # relationship
    rt = pd.read_table("./data/Graph/dblp100%_vertices.txt", header=None) # 992,5613
    print(len(rt))
    rt2 = pd.read_table("./data/Graph/dblp20%_vertices.txt", header=None) # 39,3962
    print(len(rt2))
    # node
    rt3 = pd.read_table("./data/node.csv", header=None)  # 210,1224
    print(len(rt3))

def writeRelationship(in_path,out_path):
    # 写csv
    out_csv_file = open(out_path, "a+", newline='')
    out_writer = csv.writer(out_csv_file)
    out_scheme = ("start", "end") # 边
    out_writer.writerow(out_scheme)
    # 读取 graph
    df = pd.read_table(in_path, header=None)
    for index, row in df.iterrows():
        print(row[0])
        print(row[1])
        out_writer.writerow((row[0], row[1]))
    out_csv_file.close()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    in_path = "./data/Graph/dblp100%_vertices.txt"
    out_path = "./data/relationship100.csv"
    writeRelationship(in_path, out_path)

    in_path = "./data/Graph/dblp20%_vertices.txt"
    out_path = "./data/relationship20.csv"
    writeRelationship(in_path, out_path)