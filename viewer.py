import cv2
import csv
import glob

def convertToCoordinates(baseX, baseY, baseX2, baseY2, baseWidth, baseHeight, newWidth, newHeight):
    # get the scale factors for the new image compared to the original test image
    widthScale = float(newWidth) / float(baseWidth)
    heightScale = float(newHeight) / float(baseHeight) 

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

if __name__ == "__main__":
    print("Looking through images directory for files")
    # get a list of all downloaded images
    downloadedImages = glob.glob('images/*.jpg', recursive=True)


    # loop through all files and remove the directory location and file ending
    for i in range(len(downloadedImages)):
        downloadedImages[i] = downloadedImages[i].replace("images/", "").replace(".jpg", "")
    
    print("Found {} images".format(len(downloadedImages)))
    print("Looping through cropped images")


    # loop through all files that were found
    for filename in downloadedImages:
        # read in an image (in color)
        img = cv2.imread('images/{}.jpg'.format(filename), cv2.IMREAD_COLOR)
        month = filename[0:3]
        year = filename[4:]

        newHeight = img.shape[0]
        newWidth = img.shape[1]

        baseHeight = 1239
        baseWidth = 1755 
        baseX = 1026
        baseY = 106
        baseX2 = 1476
        baseY2 = 372

        coords = convertToCoordinates(baseX, baseY, baseX2, baseY2, baseWidth, baseHeight, newHeight, newWidth)

        # crop the image to focus on the Limpopo region
        crop_img = img[coords[1]:coords[3], coords[0]:coords[2]]

        # get the dimensions of the cropped image
        height = crop_img.shape[0]
        width = crop_img.shape[1] 

        print("Showing: {}\tSize:{}x{}".format(filename, width, height))
        cv2.imshow("{}-{}".format(month, year, width, height), crop_img)
        cv2.waitKey(0)