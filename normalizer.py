import csv
import glob

# using minmax for normalization
def normalize(value):
    # define the max and min available for the dataset for minmax normalization
    dataMax = 350
    dataMin = 5

    return (float(value) - dataMin) / (dataMax - dataMin)

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

if __name__ == "__main__":
    months = ['jan', "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

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
                formattedDate = "{}-{}-{}".format(months.index(month), day+1, year)
                for data in oldData:
                    tableRows.append([formattedDate, data[0], data[1], data[2]])

        
        # open filename with write permissions as a csv file to write all the table data into the filename csv
        with open("normalized_data/{}".format(filename), 'w') as newcsvfile:
            csvwriter = csv.writer(newcsvfile)
            csvwriter.writerows(tableRows)                    


            