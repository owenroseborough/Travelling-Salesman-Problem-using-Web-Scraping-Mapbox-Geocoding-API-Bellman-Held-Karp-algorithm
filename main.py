# Travelling Salesman Project by Owen Roseborough
# held-karp algorithm implementation by CarlEkerot on GitHub
# Started on March 2, 2023
import math
import itertools

from selenium import webdriver
import requests


def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)
    print("transition costs from initial states set")

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    count = 0
    for subset_size in range(2, n):
        print(count)
        for subset in itertools.combinations(range(1, n), subset_size):

            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)
        count += 1

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))


# Press the green button in the gutter to run the script
if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get("https://www.zolo.ca/london-real-estate/page-1")
    mainElements = driver.find_elements_by_xpath("/html/body/main/section/div/span/strong")
    numPages = int((int(mainElements[1].text) / 36) + 1)

    # now we open pages 1 through 28 and scrape data from them
    index = 1
    urlPartial = "https://www.zolo.ca/london-real-estate/page-"
    roughAddressList = []
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
                roughAddressList.append(string)
                string = ""
            else:
                string += x.text + ","
            counter += 1
        urlPartial = urlPartial[0:44]
        index += 1
    driver.close()
    # now addressList contains all houses for sale on Zolo in London, Ontario, Canada
    # we need to convert these addresses to longitude and latitude GPS coordinates
    addressCoordsDict1 = {}
    addressCoordsDict2 = {}
    addressCoordsDict3 = {}
    addressCoordsDict4 = {}
    firstPartUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    secondPartUrl = "%2C%20London%2C%20Ontario%2C%20Canada.json?" \
                    "proximity=ip&access_token=pk.eyJ1Ijoib3dlbnJvc2Vib3JvdWdoIiwiYSI6ImN" \
                    "sZmxvbmY4dDAzeGszcXF6NWpucm5rdzIifQ.Q5TBzrtCfGjN0jJQSc0IeA"
    addressList1 = []
    addressList2 = []
    addressList3 = []
    addressList4 = []
    for x in roughAddressList:
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
        if response.status_code == 200:
            response_json = response.json()
            if response_json is not None and "features" in response_json and len(response_json["features"]) > 0:
                coordinates = response_json["features"][0]["geometry"]["coordinates"]
                # print(coordinates)
                if coordinates[1] < 42.984924 and coordinates[0] < -81.245277:
                    addressCoordsDict1.update({address[0]: coordinates})
                    addressList1.append(address[0])
                elif coordinates[1] > 42.984924 and coordinates[0] < -81.245277:
                    addressCoordsDict2.update({address[0]: coordinates})
                    addressList2.append(address[0])
                elif coordinates[1] < 42.984924 and coordinates[0] > -81.245277:
                    addressCoordsDict3.update({address[0]: coordinates})
                    addressList3.append(address[0])
                elif coordinates[1] > 42.984924 and coordinates[0] > -81.245277:
                    addressCoordsDict4.update({address[0]: coordinates})
                    addressList4.append(address[0])

    distanceMatrix1 = [[0 for _ in range(len(addressList1))] for _ in range(len(addressList1))]
    distanceMatrix2 = [[0 for _ in range(len(addressList2))] for _ in range(len(addressList2))]
    distanceMatrix3 = [[0 for _ in range(len(addressList3))] for _ in range(len(addressList3))]
    distanceMatrix4 = [[0 for _ in range(len(addressList4))] for _ in range(len(addressList4))]
    # fill distanceMatrix1
    row = 0
    col = 0
    for x in distanceMatrix1:
        for y in x:
            if col != row:
                longitude = math.pow(addressCoordsDict1.get(addressList1[row])[0] - addressCoordsDict1.get(addressList1[col])[0],2)
                latitude = math.pow(addressCoordsDict1.get(addressList1[row])[1] - addressCoordsDict1.get(addressList1[col])[1],2)
                distanceMatrix1[row][col] = math.sqrt(longitude + latitude)
            else:
                distanceMatrix1[row][col] = 0
            col += 1
        col = 0
        row += 1
    # fill distanceMatrix2
    row = 0
    col = 0
    for x in distanceMatrix2:
        for y in x:
            if col != row:
                longitude = math.pow(
                    addressCoordsDict2.get(addressList2[row])[0] - addressCoordsDict2.get(addressList2[col])[0], 2)
                latitude = math.pow(
                    addressCoordsDict2.get(addressList2[row])[1] - addressCoordsDict2.get(addressList2[col])[1], 2)
                distanceMatrix2[row][col] = math.sqrt(longitude + latitude)
            else:
                distanceMatrix2[row][col] = 0
            col += 1
        col = 0
        row += 1
    # fill distanceMatrix3
    row = 0
    col = 0
    for x in distanceMatrix3:
        for y in x:
            if col != row:
                longitude = math.pow(
                    addressCoordsDict3.get(addressList3[row])[0] - addressCoordsDict3.get(addressList3[col])[0], 2)
                latitude = math.pow(
                    addressCoordsDict3.get(addressList3[row])[1] - addressCoordsDict3.get(addressList3[col])[1], 2)
                distanceMatrix3[row][col] = math.sqrt(longitude + latitude)
            else:
                distanceMatrix3[row][col] = 0
            col += 1
        col = 0
        row += 1
    # fill distanceMatrix4
    row = 0
    col = 0
    for x in distanceMatrix4:
        for y in x:
            if col != row:
                longitude = math.pow(
                    addressCoordsDict4.get(addressList4[row])[0] - addressCoordsDict4.get(addressList4[col])[0], 2)
                latitude = math.pow(
                    addressCoordsDict4.get(addressList4[row])[1] - addressCoordsDict4.get(addressList4[col])[1], 2)
                distanceMatrix4[row][col] = math.sqrt(longitude + latitude)
            else:
                distanceMatrix4[row][col] = 0
            col += 1
        col = 0
        row += 1

    # Print distance matrix 1
    # for tempRow in distanceMatrix1:
    #    for entry in tempRow:
    #        format_float = "{:.14f}".format(entry)
    #        print(format_float, " ", end='')
    #    print()

    tupleCostPath1 = held_karp(distanceMatrix1)
    tupleCostPath2 = held_karp(distanceMatrix2)
    tupleCostPath3 = held_karp(distanceMatrix3)
    tupleCostPath4 = held_karp(distanceMatrix4)
    print("first path: ")
    print(tupleCostPath1)
    print("second path: ")
    print(tupleCostPath2)
    print("third path: ")
    print(tupleCostPath3)
    print("fourth path: ")
    print(tupleCostPath4)
