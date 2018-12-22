#creating kml file of drone path

import csv
import simplekml

dframe, dlat, dlon =[], [], []
lines= []
dtemp= []
ctr=0

#extracting data from srt file for drone frame number ond coordinates
with open ('C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\videos\\0301.txt','rt') as in_file:
     for line in in_file:
        ctr=ctr+1
        if ctr%4 == 1:
            dtemp1=line.strip()
            dframe.append(dtemp1)#frame number
        elif ctr%4 == 3:
            dtemp= line.split(',')
            dlat.append(dtemp[0])#latitude 
            dlon.append(dtemp[1])#longitude
            dtemp=[]

#craeting an object of simplekml
kml=simplekml.Kml()

#adding values to kml object
for i in range(len(dframe)):
    kml.newpoint(name=dframe[i], coords=[(dlat[i],dlon[i])])

#saving to check.kml file
kml.save('check.kml')
