import cv2
import csv
import glob
import time

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
    print("Looking through images directory for files")
    # get a list of all downloaded images
    downloadedImages = glob.glob('images/*.jpg', recursive=True)


    # loop through all files and remove the directory location and file ending
    for i in range(len(downloadedImages)):
        downloadedImages[i] = downloadedImages[i].replace("images/", "").replace(".jpg", "")
    
    print("Found {} images".format(len(downloadedImages)))
    print("Processing the data")

    downloadedImages = ['dec-2015']

    # loop through all files that were found
    for filename in downloadedImages:
        # read in an image (in color)
        img = cv2.imread('images/{}.jpg'.format(filename), cv2.IMREAD_COLOR)

        # crop the image to focus on the Limpopo region
        crop_img = img[106:372, 1026:1476]

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
                #if closestRange != "WHITE" and closestRange != "BLACK":
                tableRows.append([latitude, longitude, closestRange])



        # open filename with write permissions as a csv file to write all the table data into the filename csv
        with open("processed_data/{}.csv".format(filename), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(tableRows)

    print("Finished data processing. Check out the results under the processed_data directory")
