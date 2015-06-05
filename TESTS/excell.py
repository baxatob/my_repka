#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from xlwt import Workbook

data = [{"A1":111, "B1":112, "C1":113, "D1":114, "E1":115},
        {"A1":221, "B1":222, "C1":223, "D1":224, "E1":225},
        {"A1":331, "B1":332, "C1":333, "D1":334, "E1":335},
        {"A1":441, "B1":442, "C1":443, "D1":444, "E1":445},
        {"A1":551, "B1":552, "C1":553, "D1":554, "E1":555}]

book = Workbook(encoding='utf-8')
sheet1 = book.add_sheet('Sheet 1')

"""for i in range(10):
    for j in range(10):
        if i == 0:
            sheet1.write(i,j,'header%s' % j)
        else: sheet1.write(i,j,'content %s%s' % (i, j))"""

# Headers:
for j in range(len(data)):
    sheet1.write(0,j, data[0].keys()[j])

# Content:        
for i in range(len(data)):
    for j in range(len(data)):
        sheet1.write(i+1,j, data[i][data[i].keys()[j]])

book.save('simple.xls')