# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul


This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import division
import csv, pickle 
import numpy as np

communeDict = {}
fileName = 'zone_apl_2006.csv'

reader = csv.reader(open(fileName), delimiter = ";")

#% PSDC99          population sans double compte 99
#% Pop_mun_2006    population municipale 2006

row_is_header = True
nrows = 0 
for row in reader:
    if row_is_header:
        header_list = row
        row_is_header = False
    else:
        nrows += 1

row_is_header = True
for header in header_list:    
    header_index = header_list.index(header)            
    row_is_header = True
    reader = csv.reader(open(fileName), delimiter = ";")
    data_index = 0
    for row in reader:
        if row_is_header is not True:
            communeDict[header][data_index] = int(row[header_index])
            data_index += 1
            
        if row_is_header:
            communeDict[header] = np.zeros(nrows, dtype= np.int32)
            row_is_header = False
            data_index = 0


#% M.POL99 de 1 à  4
#% REG de    11 à 94
#% TAU99      0 à 10
#% TU99       0 à  8
#% zone
#

# Build code an array of unique combnation of POL99, REG, TAU99, TU99
# zcode adds Z in front of code
unsorted_zcode = (communeDict['Zone']      + 
                  1e1*communeDict['TU99']  + 
                  1e2*communeDict['TAU99'] + 
                  1e4*communeDict['REG']   + 
                  1e6*communeDict['POL99'])
unsorted_code = np.floor(unsorted_zcode/10)

#% On élimine les doublons
zcode = np.unique(np.sort(unsorted_zcode))
code_vec = np.floor(zcode/10)
unique_code_vec, code_indices, code_inverse = np.unique(code_vec, return_index=True, return_inverse=True)

zone={}
pop = communeDict['Pop_mun_2006']
for code, code_index in zip(unique_code_vec, code_indices):
    if (code_vec == code).sum() == 1: # unambiguous choice
        zone[int(code)] = int(np.mod(zcode[code_index],10));        
    else:
        zone[int(code)] = {}
        prob = np.zeros(3)
        total_pop = pop[unsorted_code == code].sum()
        for i in [1,2,3]:
            indices = ((unsorted_code == code) & ((np.mod(unsorted_zcode,10))==i)) 
            prob[i-1] = pop[indices].sum()/total_pop            
            zone[int(code)].update({i: prob[i-1]})
print zone
print len(zone)

outputFile = open("zone_apl_imputation_data", 'wb')
pickle.dump(zone, outputFile)
outputFile.close()

        #for code in zone.keys():
#    if code == 382000:
#        print code
#        print zone[code]
#        print isinstance(zone[code], int)
#        print zone[code][1]