import urllib.request

months = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "nov", "dec"}
years = {"2012", "2013", "2014", "2015", "2017", "2018", "2019", "2020"}

urllib.request.urlretrieve("https://www.weathersa.co.za/images/RainMaps/mmrain{}{}.jpg".format(months[j], year[i]), "{}{}-filename.jpg".format(months[j], year[i]))