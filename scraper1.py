from bs4 import BeautifulSoup
from urllib2 import urlopen
import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE1 = os.path.join(PROJECT_ROOT, 'dbs', 'liquorstores.db')

# TOGGLE ON/OFF TO GRAB AND SAVE HTML TO PARSE

filename = 'saved_html/liquorstores1.html'

html_file = open(filename,'w')
page = urlopen('http://www.finewineandgoodspirits.com/webapp/wcs/stores/servlet/FindStoreView?storeId=10051&langId=-1&catalogId=10051&pageNum=1&listSize=100&latitude=null&longitude=null&category=&city=&zip_code=&county=51&storeNO=').read()
html_file.write(page)
html_file.close()

conn = sqlite3.connect(DATABASE1)
c = conn.cursor()

page = open(filename)
soup = BeautifulSoup(page,'html.parser') #the standard parser was fooled by broken html and only returned 42 of 52 items
page.close()

try:
	c.execute('DROP TABLE liquorstores')
finally:
	c.execute('CREATE TABLE liquorstores (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, store_id INT, address TEXT, zipcode INT, store_type TEXT, longitude REAL, latitude REAL, google_address TEXT)')

rows = soup.find_all(class_="tabContentRow")

print "length:" # For debugging purposes
print len(rows)
for row in rows:

	try:
		address_section = row.find(class_="columnAddress")
		store_id_section = address_section.find(class_="boldMaroonText")
		store_id = int(store_id_section.text.strip())
	except:
		store_id = None
	try:
		actual_address_section = address_section.find(class_="normalText")
		address = actual_address_section.text.strip().split('Phone')[0][:-1]
		zipcode = int(address[-10:-5])
	except:
		address = None
		zipcode = None
	try:
		store_type_section = row.find(class_="columnTypeOfStore")
		store_type = store_type_section.text.strip()

		if store_type=='':
			store_type = 'Regular Collection'
	except:
		store_type = None
	try:
		location_section = row.find(class_="columnDistance")
		longitude = location_section.find(attrs={'name':'longitude'})['value']
		latitude = location_section.find(attrs={'name':'latitude'})['value']
		google_address = location_section.find(attrs={'name':'googleAddress'})['value']
	except:
		longitude = None
		latitude = None
		google_address = None

	if store_id or address or store_type or longitude or latitude or google_address:
		c.execute('INSERT INTO liquorstores (store_id, address, zipcode, store_type, longitude, latitude, google_address) VALUES (?, ?, ?, ?, ?, ?, ?)',[store_id, address, zipcode, store_type, longitude, latitude, google_address])
		conn.commit()
	else:
		print row



c.close()


