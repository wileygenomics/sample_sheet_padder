#!/usr/bin/env python
#updated 20230314 for better padding of index 2 and appropriate "no index" index.

import csv
import sys

if not len(sys.argv) == 3:
        sys.stdout.write('Usage: python s4_sheet_padder_v2.py [Initial sample-sheet.csv] [Padded sample-sheet.csv]' + '\n' + '\n')
        exit()


in_sheet = sys.argv[1]
out_sheet = open(sys.argv[2], "w", newline='', encoding='utf-8')

pads = ["ATCTCGTATG","GTGTAGATCTCG","AGATCTCGGT"]

def i1padder(index):
        unpadded_i1 = index
        fullpad = pads[0]
        current_length = len(unpadded_i1)
        bases_short = 10 - current_length
        needed_pad = fullpad[:bases_short]
        padded_i1 = unpadded_i1 + needed_pad
        return(padded_i1)
        
        
def i2padder(index):
        unpadded_i2 = index
        fullpad = pads[1]
        current_length = len(unpadded_i2)
        bases_short = 10 - current_length
        needed_pad = fullpad[:bases_short]
        padded_i2 = unpadded_i2 + needed_pad
        return(padded_i2)
        

#write headers to the padded sample sheet
out_sheet.write('[Data],,,,,' + '\n')                           
out_sheet.write('Lane,Sample_Name,Sample_ID,Index,Index2,Sample_Project' + '\n')
writer = csv.writer(out_sheet, dialect='unix',quoting=csv.QUOTE_MINIMAL)

with open(in_sheet) as short_sheet: #read through the original sample sheet
        short_sheet_reader = csv.reader(short_sheet)
        for row in short_sheet_reader:
                if not row[0].isdigit(): #sample lines must start with lane number
                        continue
                if len(row[3]) + len(row[4]) == 20: #assuming the indices are each 10bp long
                        writer.writerow(row)
                if 'SI-' in row[3]: #passing though 10X index identifiers
                        writer.writerow(row)            
                if not len(row[3]) + len(row[4]) == 20: #the lines we need to pad
                        if not len(row[3]) == 10:
                                new_i1 = i1padder(row[3])
                                row[3] = new_i1
                        if len(row[4]) == 0:
                        		new_i2 = pads[2] 
                        		row[4] = new_i2
                        if not len(row[4]) == 10:
                                new_i2 = i2padder(row[4])
                                row[4] = new_i2
                        writer.writerow(row)


        
short_sheet.close()
out_sheet.close()  