# import all the required modules
from csv import writer
from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient

# set api-client to avoid amazon algorithm, to prevent us from scrapping

client = ScrapingAntClient(token='05210b3867584fe68097020b36b21065')

# list to store extracted products in form of dictionary
data = []


# writing extracted products into data list
def writedata(purl=None, title=None, price=None, rating=None, review=None):
	data.append({'Product url': f'https://www.amazon.in{purl}', 'Product Name': f'{title}', 'Product Price': f'{price}',
				 'Rating': f'{rating}', 'Review': f'{review}'})


# write all the extracted information into the csv files
def writetofile():
	with open('products.csv', 'w') as f:
		wr = writer(f)
		wr.writerow(['Product url', 'Product Name', 'Product Price', 'Rating', 'Review', 'Product Description', 'ASIN',
					 'Manufacturer'])

		for i in data:
			wr.writerow([i['Product url'], i['Product Name'], i['Product Price'], i['Rating'], i['Review'],
						 i['Product Description'], i['ASIN'], i['Manufacturer']])


# function to check whether, the product already present in the data list or not
def checkduplicate(pr):
	for D in data:
		if D['Product url'] == pr:
			return False
	return True


# extract the products, from products listings pages
def extractproducts(pgurl):
	try:
		# request the webpage, using scrapingant-api parse its html using html parser
		pager = client.general_request(pgurl)
		soup = BeautifulSoup(pager.content, 'html.parser')

		# extracting the desired information from its specific class
		items = soup.findAll('div', attrs={
			'class': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right'})
		ad_items = soup.findAll('div', attrs={
			'class': 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col sg-col-12-of-16 s-widget-spacing-large'})

		# traversing through multiples items, shown and extracting desired information
		for i in ad_items:
			try:
				soup_ad = BeautifulSoup(str(i), 'html.parser')
				purl = soup_ad.findAll('a', attrs={
					'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
				title = soup_ad.findAll('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
				price = soup_ad.findAll('span', attrs={'class': 'a-offscreen'})
				rating = soup_ad.findAll('span', attrs={'class': 'a-icon-alt'})
				review = soup_ad.findAll('span', attrs={'class': 'a-size-base s-underline-text'})
				for j in range(len(title)):
					if checkduplicate(purl[j]['href']):
						try:
							writedata(f"{purl[j]['href']}", title[j].text, price[j].text, rating[j].text,
									  review[j].text)
						except Exception as e:
							print(e)

			except Exception as e:  # throwing error if something goes wrong
				print(e)

		for i in items:
			try:
				soup = BeautifulSoup(str(i), 'html.parser')
				purl = soup.findAll('a', attrs={
					'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
				title = soup.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
				price = soup.find('span', attrs={'class': 'a-offscreen'})
				rating = soup.find('span', attrs={'class': 'a-icon-alt'})
				review = soup.find('span', attrs={'class': 'a-size-base s-underline-text'})
				if checkduplicate(purl[0]['href']):
					try:
						writedata(f"{purl[0]['href']}", title.text, price.text, rating.text, review.text)
					except Exception as e:
						print(e)
			except Exception as e:
				print(e)

	except Exception as e:
		print(e)


# extracting desired information from individual product pages, through similar method and approach as extracting
# products form product listing page.
def extractproductdetail(purl):
	try:
		# request the webpage, using proxies and headers and parse its html using html parser
		pager = client.general_request(purl)
		soup = BeautifulSoup(pager.content, 'html.parser')

		desc = soup.find('ul', attrs={'class': 'a-unordered-list a-vertical a-spacing-mini'})
		asin = ''
		manfu = ''
		souplist = soup.find('ul',
							 attrs={'class': 'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'})
		asinlist = BeautifulSoup(str(souplist), 'html.parser')
		asinitem = asinlist.findAll('span', attrs={'class', 'a-list-item'})

		for i in asinitem:
			try:
				if 'ASIN' in i.text:
					num = i.text[i.text.index(':') + 1:]
					for k in range(len(num)):
						if num[k] not in ['', '\n', ' ']:
							asin += num[k]

				if 'Manufacturer' in i.text and manfu == '':
					manname = i.text[i.text.index(':') + 1:]
					for k in range(len(manname)):
						if manname[k] not in ['', '\n', ' ']:
							manfu += manname[k]
			except Exception as e:
				print(e)

		try:
			if asin == '' or manfu == '':
				souplist = soup.find('table', attrs={'class', 'a-keyvalue prodDetTable'})
				asinlist = BeautifulSoup(str(souplist), 'html.parser')
				asinitem = asinlist.findAll('tr')
				for i in asinitem:
					if 'ASIN' in i.text and asin == '':
						asin = i.text.strip('ASIN')
					if 'Manufacturer' in i.text and manfu == '':
						manfu = i.text.strip('Manufacturer')
		except Exception as e:
			print(e)
		manfu = manfu.replace('  ', '')
		manfu = manfu.replace('\n', '')
		manfu = manfu.replace('Manufacturer', '')
		manfu = manfu.replace('\n', '')

		if len(desc.text.strip(' ')) >= 1:
			desc = desc.text.strip(' ')
		else:
			desc = None

		if len(asin.strip('\u200e')) >= 1:
			asin = asin.strip('\u200e')
		else:
			asin = None

		if len(manfu.strip('\u200e')) >= 1:
			manfu = manfu.strip('\u200e')
		else:
			manfu = None

		return [desc, asin, manfu]

	except Exception as e:
		print(e)


# running loop, number of pages requested and extracted products from depends on number of run in loop
for page in range(1, 21):
	url = f'https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1690263838&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}'
	extractproducts(url)

# this loop depends upon number of products extracted from app pages extracted from above loop
for d in data:
	update = extractproductdetail(d['Product url'])

	if type(update) == type(None):
		print(update)
		d.update({'Product Description': None, 'ASIN': None, 'Manufacturer': None})
	else:
		d.update({'Product Description': update[0], 'ASIN': update[1], 'Manufacturer': update[2]})

# writing all the product information in a file
writetofile()
print('! FILE CREATED !')
