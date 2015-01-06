import sqlite3
import os
import requests
import time


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE1 = os.path.join(PROJECT_ROOT, 'dbs', 'licensees.db')

conn = sqlite3.connect(DATABASE1)
c = conn.cursor()


c.execute('SELECT lid, address FROM licensees')

licensees = c.fetchall()

print len(licensees)

baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAvKwvspSGZpSMVBb9Jd3d4XhqatESwWZ0&address='

count = 0

for licensee in licensees:
	lid = licensee[0]
	address = licensee[1]

	
	fullurl = baseurl + address

	page = requests.get(fullurl)

	if page.json()['results']:

		latitude = page.json()['results'][0]['geometry']['location']['lat']
		longitude = page.json()['results'][0]['geometry']['location']['lng']


		print 'Latitude:'
		print latitude
		print 'Longitude:'
		print longitude

		c.execute('UPDATE licensees SET latitude = ?, longitude = ? WHERE lid = ?', [latitude, longitude, lid])
		conn.commit()

	count = count + 1

	print count

	time.sleep(.2) #seconds


c.close()

