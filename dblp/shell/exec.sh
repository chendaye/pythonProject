#!/bin/bash
# eror: /bin/bash^M: bad interpreter ==> :set ff=unix

chmod +x ./*
pip3 install pandas
pip3 install nltk
cp -r ./nltk_data ~/
python3 ./keywords.py  # python3