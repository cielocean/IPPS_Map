import csv

filename = 'Data/IPPS' #input filename

with open (filename,'rb') as csvfile:
	reader=csv.reader(csvfile)
	new_rows = []
	header=[]
	number_of_data=100 #number of data per file
	j=1 #data file number

	for i,row in enumerate(reader):
		if i==0:
			header=row
		i=i%number_of_data
		new_row=row
		new_rows.append(new_row)
		if i==0:
			datafile = 'Data/data'+str(j)
			j=j+1
		if i==number_of_data-1:
			with open (datafile,'wb') as csvfile:
				writer=csv.writer(csvfile)
				writer.writerows(new_rows)
			new_rows=[header]
