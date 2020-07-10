# South-African-Weather-Service-Precipitation
Scrape, process, and normalize precipitation image data from the South African Weather Service for use in modeling.

The source of the data can be found at this address, https://www.weathersa.co.za/
This project should first download the raw image files, crop the images for the limpopo region, then convert the cropped images into csv files, then normalize the data in the csv files.

The first part of the process is downloading the images, which is accomplished by the scraper.
```
usage: scraper.py 
```

Next, the processor will process all the images with the correct latitude, longitude, and precipitation range and store the results in a csv file for each image.
```
usage: processor.py 
```

The last part of the process is normalizing the data in the csv files using the normalizer.
```
usage: normalizer.py 
```

NOTE: These processes must be ran in the above order to ensure that each process has the right data to work on.
