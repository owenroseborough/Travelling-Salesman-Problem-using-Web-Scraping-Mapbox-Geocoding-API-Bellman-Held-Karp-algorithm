# Travelling Salesman Project by Owen Roseborough
# Started on March 2, 2023

from selenium import webdriver
import requests

# Press the green button in the gutter to run the script
if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get("https://www.zolo.ca/london-real-estate/page-1")
    mainElements = driver.find_elements_by_xpath("/html/body/main/section/div/span/strong")
    numPages = int((int(mainElements[1].text) / 36) + 1)

    # now we open pages 1 through 28 and scrape data from them
    index = 1
    urlPartial = "https://www.zolo.ca/london-real-estate/page-"
    addressList = []
    while index <= numPages:
        urlPartial += str(index)
        # urlPartial is our webpage to scrape listings from, scrape all addresses
        driver.get(urlPartial)
        addresses = driver.find_elements_by_xpath("/html/body/main/section/div/article/div/div/a/h3/span")
        counter = 1
        string = ""
        for x in addresses:
            if counter % 3 == 0:
                string += x.text
                addressList.append(string)
                string = ""
            else:
                string += x.text + ","
            counter += 1
        urlPartial = urlPartial[0:44]
        index += 1
    driver.close()
    # now addressList contains all houses for sale on Zolo in London, Ontario, Canada
    # we need to convert these addresses to longitude and latitude GPS coordinates
    addressCoordsDict = {}
    firstPartUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    secondPartUrl = "%2C%20London%2C%20Ontario%2C%20Canada.json?" \
                    "proximity=ip&access_token=pk.eyJ1Ijoib3dlbnJvc2Vib3JvdWdoIiwiYSI6ImN" \
                    "sZmxvbmY4dDAzeGszcXF6NWpucm5rdzIifQ.Q5TBzrtCfGjN0jJQSc0IeA"
    for x in addressList:
        address = x.split(",")
        if "Lot" in address[0]:
            continue
        if "LOT" in address[0]:
            continue
        if "BLOCK" in address[0]:
            continue
        streetAddress = address[0].split()
        stringStreetAddress = ""
        for a in streetAddress:
            stringStreetAddress += a
            stringStreetAddress += "%20"
        stringStreetAddress = stringStreetAddress[0:len(stringStreetAddress) - 3]
        url = firstPartUrl + stringStreetAddress + secondPartUrl
        # A GET request to the API
        response = requests.get(url)
        # Print the response
        response_json = response.json()
        coordinates = response_json.get("features")[0].get("geometry").get("coordinates")
        # print(coordinates)
        # print(type(coordinates))
        addressCoordsDict.update({address[0]: coordinates})
    print(addressCoordsDict)
    # now we have dictionary with keys of street addresses and values of longitude and latitude
    # we need to calculate graph with weighted edges now
    # with the weight of each edge being the distance between the two points
    