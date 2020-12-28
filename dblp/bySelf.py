# lxml-etree读取文件
from lxml import etree

def main():
    xml = etree.parse("../data/dblp/test.xml")
    # print(type(xml))

    # 查找所有 book 节点
    rst = xml.xpath('//article')
    print(type(rst))
    print(rst.title)
    #
    # # 查找带有 category 属性值为 sport 的元素
    # rst2 = xml.xpath('//book[@category="sport"]')
    #
    # print(type(rst2))
    # print(rst2)
    #
    # # 查找带有category属性值为sport的元素的book元素下到的year元素
    # rst3 = xml.xpath('//book[@category="sport"]/year')
    # rst3 = rst3[0]
    #
    # print('-------------\n',type(rst3))
    # print(rst3.tag)
    # print(rst3.text)

if __name__ == '__main__':
    main()