import requests
import csv
import math

API_LINK = "https://api.yelp.com/v3/businesses/search"
API_KEY = "KwPu1fYTbXJwSu6Yga_6ZX-rJ_NcNosEYmqWvdgB9cj1fIqt6tOVZ80XpjNfA0PBQtI3txh102zksT3NG9FtY6LusKjM8XDxwa4gH4Km9IB-k6wPXC4FxnJf-MGUXXYx"
DEFAULT_LOCATION = "Hillsborough County, FL"
DEFAULT_TERM = "realtor"
TERMS = [
	"realtor",
	"Buys real estate",
	"Buys properties",
	"Buys houses",
	"Buys homes",
	"Homebuyer",
	"Homebuyer llc",
	"Buys properties",
	"Cash for houses",
	"Cash for homes",
	"Sell home for cash",
	"Cash offer",
	"Buy your house",
	"Buy houses as-is",
	"Cash for your house",
	"Sell house fast",
	"Get cash for your house",
	"Cash home buyer",
	"Cash investor",
]
headers = {
			'Authorization': 'Bearer %s' % API_KEY,
		}
fina_data = []

for term in TERMS:
	url_params = {
		'term': term.replace(' ', '+'),
		'location': DEFAULT_LOCATION.replace(' ', '+'),
		'limit': 50,
		'offset': 0
	}

	data = requests.request('GET', API_LINK, headers=headers, params=url_params).json()

	for item in data.get('businesses', []):
		address = ''
		loc = item['location']

		for i in ['1', '2', '3']:
			if loc['address%s' % i]:
				address += ', %s' % loc['address%s' % i] if i != '1' else loc['address%s' % i]
		address += ', ' + loc['city']
		address += ', ' + loc['state']
		address += ', ' + loc['zip_code']

		fina_data.append({
			'name': item['name'],
			'phone': item['phone'],
			'address': address,
			'term': term
		})

	offset = 0
	total = data['total']
	total_page = int(math.ceil(int(total) / 50 if int(total) > 50 else 0))

	for i in range(0, total_page):
		url_params['offset'] += 50
		req = requests.request('GET', API_LINK, headers=headers, params=url_params).json()
		for item in req.get('businesses', []):
			address = ''
			loc = item['location']

			for i in ['1', '2', '3']:
				if loc['address%s' % i]:
					address += ', %s' % loc['address%s' % i] if i != '1' else loc['address%s' % i]
			address += ', ' + loc['city']
			address += ', ' + loc['state']
			address += ', ' + loc['zip_code']

			fina_data.append({
				'name': item['name'],
				'phone': item['phone'],
				'address': address,
				'term': term
			})

keys = ['name', 'phone', 'address', 'term']
with open('Hillsborough Cash Buyers.csv', 'w') as output_file:
	dict_writer = csv.DictWriter(output_file, keys)
	dict_writer.writeheader()
	dict_writer.writerows(fina_data)
