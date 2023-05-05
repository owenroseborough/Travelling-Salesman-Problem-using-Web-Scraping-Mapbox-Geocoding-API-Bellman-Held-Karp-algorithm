# Travelling-Salesman-Problem-using-Web-Scraping-Mapbox-Geocoding-API-Bellman-Held-Karp-algorithm
Travelling Salesman Problem with Python, Selenium Web Scraping, Mapbox Geocoding API, and Dijkstra's algorithm

Implementation of Heldman-Karp algorithm for the travelling salesman problem in the context of all the houses for sale in London, Ontario.

Script web scrapes addresses of all houses for sale in London off Zolo and then uses a Geocoding API to get the latitude and longitude 
values for each address.

We then make a distance matrix using those coordinates, it holds the distance between any two coordinates. The diagonal from top left to bottom right
is all 0's, since the distance from a coordinate to itself is 0.

On the first iteration we tried to input the distance matrix with size 900 by 900. The time complexity of the algorithm is then (900^2) * (2^900). My laptop
couldn't compute the solution in 4 hours.

On the second interation we tried splitting the city into 4 quadrants, NW,NE,SW,SE. This resulted in 4 distance matrices of approx 250 by 250 size. My laptop
still couldn't compute the solution quickly. At this point more computing power is needed. Ending the project efforts.
