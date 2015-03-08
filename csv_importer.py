"""
Testing how cvs import works
"""

import csv

DRG=[]
with open ('Data/data_1') as csvfile:
	reader=csv.DictReader(csvfile)
	for row in reader:
		if row.get('DRG Definition') not in DRG:
			DRG.append(row.get('DRG Definition'))
	print DRG
	csvfile.seek(0)
	reader=csv.DictReader(csvfile)
	for line in DRG:
		print line
		csvfile.seek(0)
		for row in reader:
			if row.get('DRG Definition')==line:
				pass