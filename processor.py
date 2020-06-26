import cv2
import numpy as np
from matplotlib import pyplot as plt
import csv

img = cv2.imread('apr-2012.jpg', cv2.IMREAD_COLOR)

crop_img = img[106:372, 1026:1476]
cv2.imshow("cropped", crop_img)

cv2.waitKey(0)

height = crop_img.shape[0]
width = crop_img.shape[1] 

fields = ['Latitude', 'Longitude', 'Rainfall (mm)']
tableRows = []
# colors = []
# print("width: {}, height: {}".format(width, height))

startLong = 26.39806
startLat = 22.12056

legend = {
    "0-10": [254, 255, 53],
    "10-25": [215, 254, 65],
    "25-50": [151, 250, 0],
    "50-100": [2, 234, 0],
    "100-200": [19, 136, 156],
    "200-500": [0, 54, 126],
    "WHITE": [255, 255, 255],
    "BLACK": [0, 0, 0]
    }

for y in range(height):
    for x in range(width):
        if crop_img[y, x][0] != 255 or crop_img[y, x][1] != 255 or crop_img[y, x][2] != 255:
            latitude = y * (3.30277/height) + startLat
            longitude = x * (5.48388/width) + startLong
            tableRows.append([latitude, longitude, crop_img[y, x]])

filename = "test.csv"

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(tableRows)


    # (1026, 372), (1476, 106)
    # lat = y difference, long = x difference     
    #       left                right
    #long = 26deg23min53sec - 31deg52min55sec    E  
    #long = 26.39806 - 31.88194
    #long = 5.48388
    #       top                 bottom
    #lat = 22deg07min14sec - 25deg25min24sec     S
    #lat = 22.12056 - 25.42333
    #lat = 3.30277
