import csv
import glob
from collections import deque

# using minmax for normalization
def normalize(range):
    normalizedRanges = {
        "0-10": 0,
        "10-25": 0.0306,
        "25-50": 0.0815,
        "50-100": 0.1837,
        "100-200": 0.4082,
        "200-500": 1,
        "WHITE": 0,
        "BLACK": 0
    }

    return normalizedRanges[range]

# returns the number of days in a month given the month and year
def getNumDaysInMonth(month, year):
    if month == "apr" or month == "jun" or month == "sep" or month == "nov":
        return 30
    elif month == "feb":
        if int(year) % 4 == 0:
            return 29
        else:
            return 28
    else:
        return 31

# returns the month number of the year
def getMonthNumber(month):
    if month == "jan":
        return 1
    elif month == "feb":
        return 2
    elif month == "mar":
        return 3
    elif month == "apr":
        return 4
    elif month == "may":
        return 5
    elif month == "jun":
        return 6
    elif month == "jul":
        return 7
    elif month == "aug":
        return 8
    elif month == "sep":
        return 9
    elif month == "oct":
        return 10
    elif month == "nov":
        return 11
    else:
        return 12

if __name__ == "__main__":
    # get a list of all data files
    dataFiles = glob.glob('processed_data/*.csv')

    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    years = ["2012", "2013", "2014", "2015", "2017", "2018", "2019", "2020"]

    fullData = deque([['Date', 'Latitude', 'Longitude', 'Rainfall (mm)']])

    for year in years:
        for month in months:  
            filename = "{}-{}.csv".format(month, year)
            filepath = "processed_data/{}".format(filename)
            if filepath in dataFiles:
                print("Found file: {}".format(filename))
                # open the csv file
                with open(filepath) as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    tmpData = []
                    lineNum = 0
                    for row in reader:
                        # skip the headers of each file
                        if lineNum != 0:
                            tmpData.append([row[0], row[1], normalize(row[2])])
                        lineNum += 1

                    numDays = getNumDaysInMonth(month, year)
                    for day in range(numDays):  
                        formattedDate = "{}-{}-{}".format(getMonthNumber(month), day+1, year)
                        
                        for data in tmpData:
                            fullData.append([formattedDate, data[0], data[1], data[2]])

            else:
                print("ERROR: Missing file: {}".format(filename))
                            

    print("Writing data to file...may take awhile")

    # open filename with write permissions as a csv file to write all the table data into the filename csv
    with open("combined_data/saws_precipitation.csv".format(filename), 'w') as newcsvfile:
        csvwriter = csv.writer(newcsvfile)
        csvwriter.writerows(fullData)

            