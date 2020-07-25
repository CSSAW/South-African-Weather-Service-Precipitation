import cv2
import csv
import glob

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

# returns the cropped coordinates of the Limpopo region in the image given the image width, height, month and year
def getRegionCoordinates(width, height, month, year):
    regionsByMonthYear = {
        ('apr', '2019'): (876, 142, 1320, 404),
        ('apr', '2020'): (1788, 260, 2706, 814),
        ('aug', '2019'): (894, 131, 1359, 410),
        ('feb', '2020'): (1752, 336, 2592, 844),
        ('jun', '2020'): (1786, 262, 2702, 814),
        ('jan', '2020'): (1756, 338, 2596, 840),
        ('jun', '2020'): (1750, 332, 2594, 842)
    }
    regionsByDimensions = {
        (1755, 1239): (1026, 106, 1476, 372),
        (1100, 850): (561, 116, 839, 281),
        (3300, 2550): (1689, 352, 2516, 852), 
        (1650, 1275): (841, 177, 1256, 426),
        (1056, 816): (541, 111, 806, 271), 
        (1320, 1020): (672, 141, 1004, 337),
        (9350, 6617): (5356, 852, 7468, 2084),
        (1169, 827): (687, 41, 1006, 227), 
        (1122, 794): (651, 46, 954, 222), 
        (1430, 1105): (729, 153, 1088, 368),
        (6655, 5142): (3399, 708, 5060, 1700),
        (1753, 1241): (1038, 59, 1521, 348),
        (994, 768): (506, 106, 755, 257) 
    }
    if (month, year) in regionsByMonthYear:
        return regionsByMonthYear[(month, year)]
    else:
        return regionsByDimensions[(width, height)]


# converts an x, y coordinate in the image of size width x height to a latitude, longitude coordinate
def convertToCoordinate(x, y, width, height):
    # the starting latitude and longitude of the square that encloses the Limpopo region (calculated using Google Earth)
    startLong = 26.39806
    startLat = 22.12056

    # calculate the latitude and longitude based off of pixel location and conversion rate (calculated using Google Earth)
    latitude = y * (3.30277/height) + startLat
    longitude = x * (5.48388/width) + startLong

    return latitude, longitude

# gets a sampling of a region of pixels and returns the average value
def getSample(img, x, y, xEnd, yEnd):
    rangeToValue = {
        "0-10": 5,
        "10-25": 17.5,
        "25-50": 37.5,
        "50-100": 75,
        "100-200": 50,
        "200-500": 350,
    }

    pixelX = x
    pixelY = y

    totalValues = 0
    numValues = 0
    # loop through the sample region to calculate an average
    while pixelY <= yEnd:
        while pixelX <= xEnd:
            # convert the gbr pixel to be rgb
            pixel = (img[pixelY, pixelX][2], img[pixelY, pixelX][1], img[pixelY, pixelX][0])

            # get the colosest rainfall range (in mm) 
            closestRange = getClosestRange(pixel)

            # make sure data is not garbage
            if closestRange != "WHITE" and closestRange != "BLACK":
                # get the value for the range and add it to totalValues
                totalValues += rangeToValue[closestRange]
                numValues += 1
            pixelX += 1
        pixelY += 1

    # return the average of all non-garbage data in the region
    if numValues > 0:
        #print("SUM: {}".format(totalValues))
        return totalValues / float(numValues) 
    # return -1 if there are no values to average     
    else:
        return -1

if __name__ == "__main__":
    print("Looking through images directory for files")
    # get a list of all downloaded images
    downloadedImages = glob.glob('images/*.jpg', recursive=True)


    # loop through all files and remove the directory location and file ending
    for i in range(len(downloadedImages)):
        downloadedImages[i] = downloadedImages[i].replace("images/", "").replace(".jpg", "")
    
    print("Found {} images".format(len(downloadedImages)))
    print("Processing the data")


    # loop through all files that were found
    for filename in downloadedImages:
        # read in an image (in color)
        img = cv2.imread('images/{}.jpg'.format(filename), cv2.IMREAD_COLOR)

        # parse month and year from filename
        month = filename[0:3]
        year = filename[4:]

        print("Parsing {}-{}".format( month, year) )

        # get dimensions of original image
        width = img.shape[1]
        height = img.shape[0]

        # get coordinates of Limpopo region
        coords = getRegionCoordinates(width, height, month, year)
       
        # crop the image to focus on the Limpopo region
        crop_img = img[coords[1]:coords[3], coords[0]:coords[2]]

        #cv2.imshow("{}-{}".format(month, year, width, height), crop_img)
        #cv2.waitKey(0)

        # get the dimensions of the cropped image
        croppedHeight = crop_img.shape[0]
        croppedWidth = crop_img.shape[1] 

        #print("HEIGHT: {}".format(croppedHeight))

        # setup lists to hold data
        fields = ['Latitude', 'Longitude', 'Rainfall (mm)']
        tableRows = []

        x = 0
        y = 0

        # loop through regions of pixels in the image to create samplings of data
        while y < croppedHeight:
            #print(x, y)
            x = 0
            while x < croppedWidth: 
                #print(x,y)
                # calculate the amount of pixels left to avoid out of bounds errors
                xPixelsLeft = (croppedWidth - 1) - x
                yPixelsLeft = (croppedHeight - 1) - y

                xEnd = x + min(4, xPixelsLeft)
                yEnd = y + min(4, yPixelsLeft)

                # get latitude and longitude of the sample region being used for a data point               
                startLatitude, startLongitude = convertToCoordinate(x, y, croppedWidth, croppedHeight)
                endLatitude, endLongitude = convertToCoordinate(xEnd, yEnd, croppedWidth, croppedHeight)

                # get average latitude and longitude of the sample region to use as a data point
                averageLatitude = (startLatitude + endLatitude) / 2
                averageLongitude = (startLongitude + endLongitude) / 2
                
                avgPrecipitation = getSample(crop_img, x, y, xEnd, yEnd)
                
                # check to make sure that region has non-garbage data points before adding to table
                if avgPrecipitation != -1:
                    tableRows.append([averageLatitude, averageLongitude, avgPrecipitation])
                #print(y)

                x += 5
            y += 5

        # open filename with write permissions as a csv file to write all the table data into the filename csv
        with open("processed_data/{}.csv".format(filename), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(tableRows)

    print("Finished data processing. Check out the results under the processed_data directory")
