import cv2
import numpy as np
from matplotlib import pyplot as plt
import csv

# returns the closest range of rainfall to depending on the color of the pixel
def getClosestRange(pixel):
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

    closestRange = "WHITE"
    closestDistance = 999999999999
    
    # loop through every entry in the dictionary for the image legend
    for strRange, color in legend.items():
        # distance formula used to find distance between colors:
        #   take the cube root of the sum of the squared differences between r, g, and b values
        distance = (((pixel[0] - color[0])**2) + ((pixel[1] - color[1])**2) + ((pixel[2] - color[2])**2))**(1.0/3.0)

        # closer range was found -> update the closest distance and range variables
        if distance < closestDistance:
            closestDistance = distance
            closestRange = strRange
    
    return closestRange


if __name__ == "__main__":
    # read in an image (in color)
    img = cv2.imread('apr-2012.jpg', cv2.IMREAD_COLOR)

    # crop the image to focus on the Limpopo region
    crop_img = img[106:372, 1026:1476]
    
    # FOR DEBUGGING ONLY
    # # show the cropped image
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)

    # get the dimensions of the cropped image
    height = crop_img.shape[0]
    width = crop_img.shape[1] 

    # setup lists to hold data
    fields = ['Latitude', 'Longitude', 'Rainfall (mm)']
    tableRows = []

    # the starting latitude and longitude of the square that encloses the Limpopo region (calculated using Google Earth)
    startLong = 26.39806
    startLat = 22.12056

    # loop through each pixel in the cropped image
    for y in range(height):
        for x in range(width):
            # calculate the latitude and longitude based off of pixel location and conversion rate (calculated using Google Earth)
            latitude = y * (3.30277/height) + startLat
            longitude = x * (5.48388/width) + startLong
            
            # convert the gbr pixel to be rgb
            pixel = (crop_img[y, x][2], crop_img[y, x][1], crop_img[y, x][0])

            # get the colosest rainfall range (in mm) 
            closestRange = getClosestRange(pixel)

            # make sure the data is not garbage data before adding it to the table
            if closestRange != "WHITE" and closestRange != "BLACK":
                tableRows.append([latitude, longitude, closestRange])


    filename = "test.csv"

    # open filename with write permissions as a csv file to write all the table data into the filename csv
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
