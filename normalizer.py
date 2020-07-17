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
    dataFiles = glob.glob('processed_data/*.csv', recursive=True)

    # loop through every file in the directory
    for file in dataFiles:
        tableRows = []
        # parse the name of the file
        filename = file.replace("processed_data/", "")
        print("Normalizing {}".format(filename))
        # parse the month and year from the file name
        month = filename[0:3]
        year = filename[4:8]
        # open the csv file
        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lineNum = 0
            oldData = []
            # for every row in the file, read in the data
            for row in reader:
                # read in the column headers directly to the table rows output
                if lineNum == 0:
                    tableRows.append(['Date', row[0], row[1], row[2]])
                # read in the data from the file into oldData
                else:
                    oldData.append([row[0], row[1], normalize(row[2])])
                lineNum += 1

            # get the number of days in the current month
            numDays = getNumDaysInMonth(month, year)
            # for every day in the month, format the date and push in all relevant data for that day
            for day in range(numDays):
                formattedDate = "{}-{}-{}".format(getMonthNumber(month), day+1, year)
                for data in oldData:
                    tableRows.append([formattedDate, data[0], data[1], data[2]])

        
        # open filename with write permissions as a csv file to write all the table data into the filename csv
        with open("normalized_data/{}".format(filename), 'w') as newcsvfile:
            csvwriter = csv.writer(newcsvfile)
            csvwriter.writerows(tableRows)                    


            