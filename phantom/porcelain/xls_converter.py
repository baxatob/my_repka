#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from xlwt import Workbook

with open("PORCELAIN.json", "r") as file_:
    data = json.load(file_)

book = Workbook(encoding='utf-8')
sheet1 = book.add_sheet('Sheet 1')

#Column headers:
sheet1.write(0,0,'sale_date')
sheet1.write(0,1,'sale_name')
sheet1.write(0,2,'lot_number')
sheet1.write(0,3,'low_estimate')
sheet1.write(0,4,'high_estimate')
sheet1.write(0,5,'currency')
sheet1.write(0,6,'artist')
sheet1.write(0,7,'title')
sheet1.write(0,8,'date')
sheet1.write(0,9,'size')
sheet1.write(0,10,'unit_of_measure')
sheet1.write(0,11,'description')
sheet1.write(0,12,'literature')
sheet1.write(0,13,'source_url')
sheet1.write(0,14,'image_url')


i = 1
for el in data:
    sheet1.write(i,0, el["saleDate"])
    sheet1.write(i,1, el["saleName"])
    sheet1.write(i,2, el["lotNum"])
    sheet1.write(i,3, el["lowEstimate"])
    sheet1.write(i,4, el["highEstimate"])
    sheet1.write(i,5, el["currency"])
    sheet1.write(i,6, el["artist"])
    sheet1.write(i,7, el["title"])
    sheet1.write(i,8, el["date"])
    sheet1.write(i,9, el["size"])
    sheet1.write(i,10, el["unit"])
    sheet1.write(i,11, el["description"])
    sheet1.write(i,12, el["literature"])
    sheet1.write(i,13, el["URL"])
    sheet1.write(i,14, el["image"])
    i += 1


book.save('porcelain.xls')