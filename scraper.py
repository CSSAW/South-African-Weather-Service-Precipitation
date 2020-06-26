import urllib.request
import urllib.error
import glob
 

if __name__ == "__main__":
    months = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"}
    years = {"2012", "2013", "2014", "2015", "2017", "2018", "2019", "2020"}
    
    failedEntries = []
    images = []
    print("Starting scraper process")

    # # loop through every month in the year for each year
    for i in years:
        print("Downloading data for the year {}".format(i))
        for j in months:
            # try to download the image
            try:
                urllib.request.urlretrieve("https://www.weathersa.co.za/images/RainMaps/mmrain{}{}.jpg".format(j, i), "images/{}-{}.jpg".format(j, i))
                # keep track of the image to for later to validate all downloads were successful
                images.append("images/{}-{}.jpg".format(j, i))              
            # check for http error
            except urllib.error.HTTPError as e:
                print("Problem with downloading the following entry: {}-{}".format(j, i))
                print("Error code: {}\n".format(e.code))
                failedEntries.append("{}-{}".format(j, i))
            # check for content too short error
            except urllib.error.ContentTooShortError as e:
                print("Problem with downloading the following entry: {}-{}".format(j, i))
                print("Content not fully downloaded error")
                failedEntries.append("{}-{}".format(j, i))

    # check which files were saved to the system
    downloadedImages = []
    downloadedImages = glob.glob('images/*.jpg', recursive=True)
    attemptedDownloads = len(downloadedImages)

    # remove successful downloads to keep track of which files are missing
    for image in downloadedImages:
        images.remove(image)

    # Summary of scaper process
    print("Scraper process finished\n-----SUMMARY------")
    print("Number of attempted downloads: {}".format(attemptedDownloads))
    print("Number of failed entries: {}".format(len(failedEntries)))
    print("Failed entries:")
    for entry in failedEntries:
        print(entry)
    print("Number of missing files: {}".format(len(images)))
    print("Missing files:")
    for file in images:
        print(file[5:])
