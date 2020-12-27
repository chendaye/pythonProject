# lxml

[参考](https://github.com/ThomHurks/dblp-to-csv)

```bash
./toCSV.py --annotate --neo4j ../data/dblp/test.xml ../data/dblp/temp/dblp.dtd output.csv --relations author:authored_by journal:published_in publisher:published_by school:submitted_at editor:edited_by cite:has_citation series:is_part_of
```


# sax

[参考](https://github.com/MrKevinLu/dblp_parse/blob/master/src/lib/parse_dblp_xml.py)