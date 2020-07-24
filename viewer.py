import cv2
import csv
import glob

def convertToCoordinates(baseX, baseY, baseX2, baseY2, baseWidth, baseHeight, newWidth, newHeight):
    # get the scale factors for the new image compared to the original test image
    widthScale = float(newWidth) / float(baseWidth)
    heightScale = float(newHeight) / float(baseHeight) 
    print("NEW W={}\t\tH={}\t\tOLD W={}\t\tH={}".format(newWidth, newHeight, baseWidth, baseHeight))
    print("SCALES: W={}\t\tH={}".format(widthScale, heightScale))

    # compare the scaling of the coordinates of the original region to the size of the original image
    xScale = float(baseX) / float(baseWidth)
    yScale = float(baseY) / float(baseHeight)

    # get starting coordinates of region in new image
    newX = int(xScale * newWidth)
    newY = int(yScale * newHeight)

    # get width and height of region in new image
    newRegionWidth = int((baseX2 - baseX) * widthScale)
    newRegionHeight = int((baseY2 - baseY) * heightScale)
    
    return (newX, newY, newX+newRegionWidth, newY+newRegionHeight)

def getRegionCoordinates(width, height):
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

    return regionsByDimensions[(width, height)]

if __name__ == "__main__":
    print("Looking through images directory for files")
    # get a list of all downloaded images
    downloadedImages = glob.glob('images/*.jpg', recursive=True)


    # loop through all files and remove the directory location and file ending
    for i in range(len(downloadedImages)):
        downloadedImages[i] = downloadedImages[i].replace("images/", "").replace(".jpg", "")
    
    print("Found {} images".format(len(downloadedImages)))
    print("Looping through cropped images")

    sizes = []
    files = []

    #downloadedImages = ['apr-2012', 'apr-2013', 'apr-2014', 'apr-2015', 'aug-2012', 'aug-2015', 'dec-2015', 'jun-2012', 'may-2012', 'nov-2015', 'oct-2012', 'oct-2018', 'sep-2017']

    #went through all newly cropped image bounds and found that these need to be redone:
    #apr-2019, apr-2020, aug-2019, feb-2020, jun-2020

    # loop through all files that were found
    for filename in downloadedImages:
        # read in an image (in color)
        img = cv2.imread('images/{}.jpg'.format(filename), cv2.IMREAD_COLOR)
        month = filename[0:3]
        year = filename[4:]

        width = img.shape[1]
        height = img.shape[0]

        #coords = convertToCoordinates(baseX, baseY, baseX2, baseY2, baseWidth, baseHeight, newHeight, newWidth)
        coords = getRegionCoordinates(width, height)

        # crop the image to focus on the Limpopo region
        crop_img = img[coords[1]:coords[3], coords[0]:coords[2]]

        print("Showing: {}\tSize:{}x{}".format(filename, width, height))
        cv2.imshow("{}-{}".format(month, year, width, height), crop_img)
        cv2.waitKey(0)


