from pygeocoder import Geocoder
results = Geocoder.geocode("Tian'anmen, Beijing")
# gmaps = GoogleMaps(529796355696)
# address ='1000 Olin way'
# lat,lng = gmaps.address_to_latlng(address)
print (results[0].coordinates)

# import csv
# DRG=[]
# with open ('inpatient_provide_summary') as csvfile:
#with open ('short') as csvfile:
	# reader=csv.DictReader(csvfile)
	# for row in reader:
	# 	if row.get('DRG Definition') not in DRG:
	# 		DRG.append(row.get('DRG Definition'))
	# print DRG
	# csvfile.seek(0)
	# reader=csv.DictReader(csvfile)
	# for line in DRG:
	# 	print line
	# 	csvfile.seek(0)
	# 	for row in reader:
	# 		if row.get('DRG Definition')==line:
	# 			pass