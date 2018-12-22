from geopy import distance#to calculate geodesic distance
#between 2 points whose lat and lon are known
from math import radians
import csv
import time


#fetching the image data stored in out7.txt(exiftool has been used for this) to corresponding lists.
imageid,lat,lon =[], [], []
lines= []
temp= []
with open ('C:\\Users\\Siddharth\\out7.txt','rt') as in_file:
    for line in in_file:
        lines.append(line)
        
for element in lines:
    temp= element.split()
    #print(temp)
    
    if temp[1]=="-" or temp[2]=="-":
        continue
    imageid.append(temp[0])
    lon.append(temp[1])
    lat.append(temp[2])


#the srt file is first renamed from 0301.srt to 0301.txt for convinience
    
dt, dlat, dlon=[], [], []   #drone time, drone latitude, drone longitude
dtinsec= [] #time in seconds
dlines= []
dtemp= []
ctr= 0  #will keep track of line number
#i am using the line number to extrac the time , lat and lon parameters from srt file

#file opened and the corresponding time,lat and lon are stored in the lists dt,dlat,dlon respectively
with open ('C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\videos\\0301.txt') as in_file:
    for line in in_file:
        ctr=ctr+1
        if ctr%4 == 2:
            dt.append(line)
            dsec = line.split(":")
            dsec2 = dsec[2].split(",")
            dtinsec.append(dsec2[0]) # seconds only(if frame number has to be not taken into account)
        elif ctr%4 == 3:
            dtemp= line.split(',')
            dlon.append(dtemp[0])
            dlat.append(dtemp[1])
            dtemp=[]


noe = len(dt)#number of entries in srt file which will act as our counter here
geodist=0 #var to store geodesic dist. between pos of drone and geotagged image



                    ###first assignment###(storing images within 35 m of drone position)

#function to overwrite all previous contents and add the first line which is time in secs, image id(s)
def write_csv_firstline(data):
    with open('C:\\Users\\Siddharth\\Desktop\\pyy\\imgdata.csv', 'w', newline = '') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

#function to write the time,imgid,lat,lon of geotagged images into a csv file       
def write_csv(data):
    with open('C:\\Users\\Siddharth\\Desktop\\pyy\\imgdata.csv', 'a', newline = '') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

write_csv_firstline(['time in secs','image id(s)'])

for  i in range(len(dtinsec)):#outer loop iterates over all drone positions
    imglist= []
    imglist.append(dt[i].strip())
    for j in range(len(imageid)):#inner loop iterates over all geotagged images
        dlist= []#coordinates of drone
        ilist= []#coordinates of image
        dlist.append(float(dlat[i]))
        dlist.append(float(dlon[i]))
        ilist.append(float(lat[j]))
        ilist.append(float(lon[j]))
        geodist = distance.geodesic(dlist, ilist, ellipsoid='GRS-80').miles
        geodist=geodist*1609.34
        if geodist<=35.0:
            imglist.append(imageid[j])
    #print(imglist)        
    write_csv(imglist)#writing the time and imageid(s) lying within 35 m of the current drone position
    
##function for output in seconds

def flush_contents(data):
    with open('C:\\Users\\Siddharth\\Desktop\\pyy\\imgdata.csv', 'w+', newline = '') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)
    
def write_csv_insec(data):
    with open('C:\\Users\\Siddharth\\Desktop\\pyy\\imgdata.csv', 'a', newline = '') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

def out_seconds(start_time):
    ctrr=0
    prev = start_time
    item_list = []
    item_list.append(prev)
    with open ('C:\\Users\\Siddharth\\Desktop\\pyy\\imgdata.csv') as in_file:
        for line in in_file:#skip the first line
            if ctrr ==0:
                ctrr = ctrr+1
                continue
            
            temp2 = line.strip().split(',')
            print(temp2)
            temp1 = temp2[0].split(':')
            temp = temp1[2] #time in seconds
            print(temp)
            if(prev == temp):
                seen = set(item_list)
                for item in range(3,len(temp2)):
                    print(temp2[item])
                    if temp2[item] not in seen:
                        seen.add(temp2[item])
                        item_list.append(temp2[item])
            else:
                
                prev = temp
                imglistsecs.append(item_list)
                item_list = []
                item_list.append(temp)

        print(imglistsecs)
        
        flush_contents(imglistsecs[0])#erase all contents and add the first line i.e. time in secs and imgids
        del(imglistsecs[0])
        for i in imglistsecs:
            write_csv_insec(i)


imglistsecs = []
imglistsecs.append(['all images corresponding to t=0 have there frames within t = 0 to t = 1 sec'])
imglistsecs.append(['time in secs' , 'imgid(s)'])#list of lists actually, each nested list will contain ['time in secs', 'img ids']..and this list will be written back to csv
def start_time_finder():
    start_time = -1
    ctrr=0
    with open ('C:\\Users\\Siddharth\\Desktop\\pyy\\imgdata.csv') as in_file:
        for line in in_file:
            if ctrr == 0:
                ctrr = ctrr+1
                continue#skip the first line
            temp2 = line.split(',')
            temp1 = temp2[0].split(':')
            temp = temp1[2]
            start_time = temp
            break
    out_seconds(start_time)    

start_time_finder()#call function to get start time of srt file



                                       ####second assignment####(POI)

poiinfo, assetlat, assetlon = [],[],[]  #variables to store the parameters

#function to read point of interest data from csv file
def posdat():
    loc = ("C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\assets.csv")
    with open(loc) as poifile:
        data = [row for row in csv.reader(poifile)]

    #print(data)   
    nor=len(data)
    for i in range(1,nor):
        poiinfo.append(data[i][0])
    for i in range(1,nor):
        assetlon.append(data[i][1])
        assetlat.append(data[i][2])

posdat()#call the function to fetch data

#writing the parameters

##this snippet of code is to only get the column names
firstline= []
with open('C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\assets.csv','rt') as in_file:
    for line in in_file:
        firstline=line.strip().split(',')
        break#only read the first line to get the parameter names, 1 iteration
##

#open the csv file to overwrite all existing contents, that's why all the data has been stored for rewritting
with open('C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\assets.csv', 'w', newline = '') as outfile:
    writer = csv.writer(outfile)    
    writer.writerow(firstline)#writing the column names first

#function to write into assets.csv
def writepoi_csv(data):
     with open('C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\assets.csv', 'a', newline = '') as outfile:
        writer = csv.writer(outfile) 
        writer.writerow(data)

#adding the images along with pois
for i in range(len(assetlat)):
    
    imglist= []
    imglist.append(poiinfo[i])
    imglist.append(assetlon[i])
    imglist.append(assetlat[i])
    for j in range(len(imageid)):
        
        plist= []#coordinates of poi
        ilist= []#coordinates of image
        plist.append(float(assetlat[i]))
        plist.append(float(assetlon[i]))
        ilist.append(float(lat[j]))
        ilist.append(float(lon[j]))
        geodist = distance.geodesic(plist, ilist, ellipsoid='GRS-80').miles
        geodist=geodist*1609.34
        if geodist<=50.0:
            imglist.append(imageid[j])
    print(imglist)
    writepoi_csv(imglist)#imglist contains [ 'poi_name', lat , lon ] and is sent for writing
    

