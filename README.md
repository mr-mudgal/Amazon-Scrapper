# Amazon-Scrapper

This is an Amazon Scrapper, which uses Python Requests, and BeautifulSoup4 modules in order to request the product pages, and extract the data from them respectively.
Data extracted are:
* Product URL
* Product Name
* Product Price
* Product Description
* Ratings
* Number of Reviews
* ASIN
* Manufacturer

It extract 20 product listing pages. It then extract each single product page.

Initailly the data is stored in a dictionary variable, and then it is converted, and written into a file in CSV format.

It also uses the concept of proxies, as amazon have algorithm to detect the scrapping script, and makes its service unavailable in response to a scrapping script. Proxies, and headers, help us to simulate a real browser behaviour, hence bypassing the amazon algorithms, and allowing us to extract the data.

The whole software is divided into two parts, the first part extract products from product listing page, with their url, name, price, rating and number of review detail.
In part 2, we extract every single product page, to obtain its description, asin and manufacturer.
