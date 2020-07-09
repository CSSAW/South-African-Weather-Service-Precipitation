import csv
import glob

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

if __name__ == "__main__":
    # get a list of all data files
    dataFiles = glob.glob('processed_data/*.csv', recursive=True)

    # loop through every file in the directory
    for file in dataFiles:
        tableRows = []
        # open the csv file
        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lineNum = 0
            for row in reader:
                if lineNum == 0:
                    tableRows.append(row)
                else:
                    tableRows.append([row[0], row[1], normalize(row[2])])
                lineNum += 1
        
        filename = file.replace("processed_data/", "")
        # open filename with write permissions as a csv file to write all the table data into the filename csv
        with open("normalized_data/{}".format(filename), 'w') as newcsvfile:
            csvwriter = csv.writer(newcsvfile)
            csvwriter.writerows(tableRows)