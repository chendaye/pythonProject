# lxml

[参考](https://github.com/ThomHurks/dblp-to-csv)

```bash
./toCSV.py --annotate --neo4j ../data/dblp/test.xml ../data/dblp/temp/dblp.dtd output.csv --relations author:authored_by journal:published_in publisher:published_by school:submitted_at editor:edited_by cite:has_citation series:is_part_of
```


# sax

[参考](https://github.com/MrKevinLu/dblp_parse/blob/master/src/lib/parse_dblp_xml.py)


# 生成文件

## article.csv

```
article_id author title journal year ee mdate key publtype reviewid rating
```

## author.csv

> 节点属性： title title_id

## relationship.csv

> 边的属性：node_id  weight  other_node_id



> 图中的节点

## relationship.csv

> 图中的边

# 非法字符

- &ouml;
- &auml;
- &Uuml;

```
几个常用的方法如下:

:%s/foo/bar/g
把全部foo替换为bar,全局替换

:s/foo/bar/g
当前行替换foo为bar

:%s/foo/bar/gc
替换每个foo为bar,但需要确认.

:%s/\<foo\>/bar/gc
单词匹配替换, 需确认

:%s/foo/bar/gci
忽略foo大小写,替换为bar, 需确认
```

[正则](https://www.cnblogs.com/chenhuan001/p/7147662.html)

```bash
# vim 替换

:%s/&.*;//g

sed -i ""  's/&.*;//g'  dblp.xml
sed -i ""  's/\<\/su[pb]\>//g'  dblp.xml
sed -i ""  's/\<su[pb]\>//g'  dblp.xml



sed -i ""  's/\<i\>//g'  dblp.xml
sed -i ""  's/\<\/i\>//g'  dblp.xml


sed -i -e '38367266d' ./temp/dblp.xml

```