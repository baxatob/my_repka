#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re

with open("ansii_table.txt", 'r') as file_:
        array = file_.readlines()
        
DB = []        
for el in array:
    record = re.compile('\w+').findall(el)
    DB.append(record)
    
print len(DB)
print DB

json = []
for i in range (len(DB[0])):
    record = {DB[0][i]:[DB[1][i], DB[2][i], DB[3][i], DB[4][i], DB[5][i], DB[6][i], DB[7][i], DB[8][i], DB[9][i]]}
    json.append(record)   



print json        
