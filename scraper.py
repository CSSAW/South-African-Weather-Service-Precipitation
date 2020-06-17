import urllib.request
import urllib.error

months = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "nov", "dec"}
years = {"2012", "2013", "2014", "2015", "2017", "2018", "2019", "2020"}

missingEntries = []
print("Starting scraper process")

# loop through every month in the year for each year
for i in years:
    print("Downloading data for the year {}".format(i))
    for j in months:
        # try to download the image
        try:
            urllib.request.urlretrieve("https://www.weathersa.co.za/images/RainMaps/mmrain{}{}.jpg".format(j, i), "images/{}-{}.jpg".format(j, i))
        # check for http error
        except urllib.error.HTTPError as e:
            print("Problem with downloading the following entry: {}-{}".format(j, i))
            print("Error code: {}\n".format(e.code))
            missingEntries.append("{}-{}".format(j, i))
        # check for content too short error
        except urllib.error.ContentTooShortError as e:
            print("Problem with downloading the following entry: {}-{}".format(j, i))
            print("Error msg: {}\n".format(e.msg))
            missingEntries.append("{}-{}".format(j, i))

# Summary of scaper process
print("Scraper process finished\n-----SUMMARY------")
print("Missing entries:")
for entry in missingEntries:
    print(entry)



