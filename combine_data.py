"""
Combine parsed csv data in different files into one single file
"""
import csv

compiled_file = 'Data/IPPSlatlon'
filenumber = 70 #number of files to compile

for i in range(1,filenumber+1):
	datafile = 'Data/data' + str(i) + 'latlon'

	with open (datafile,'rb') as csvfile:
		reader=csv.reader(csvfile)

		for j,row in enumerate(reader):
			if j==0:
				if i==1:
					header=row
					compiled_rows=[header] #create list for all data
				continue #pass header of each file unless it is the first file
			compiled_rows.append(row)

with open (compiled_file,'wb') as csvfile:
	writer=csv.writer(csvfile)
	writer.writerows(compiled_rows)

