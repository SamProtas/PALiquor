import os
import pandas as pd
import numpy as np 
import sqlite3
import requests
import time

def fix_location(lid, new_address):
    
    pd.set_option('display.mpl_style', 'default')
    
    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
    DATABASE1 = os.path.join(PROJECT_ROOT, 'dbs', 'licensees.db')
    
    conn1 = sqlite3.connect(DATABASE1)
    c = conn1.cursor()
    
    c.execute('SELECT address, latitude, longitude FROM licensees WHERE lid = ?',[lid])
    
    old_info = c.fetchone()
    old_latitude = old_info[1]
    old_longitude = old_info[2]
    
    if old_latitude or old_longitude:
        return 'No need to fix. Aborting geocode call.'
    
    baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAvKwvspSGZpSMVBb9Jd3d4XhqatESwWZ0&address='
    fullurl = baseurl + new_address

    page = requests.get(fullurl)
    
    latitude = page.json()['results'][0]['geometry']['location']['lat']
    longitude = page.json()['results'][0]['geometry']['location']['lng']
    
    c.execute('UPDATE licensees SET address = ?, latitude = ?, longitude = ? WHERE lid = ?',[new_address, latitude, longitude, lid])    

    conn1.commit()
    c.close()
    
    return 'Good Fix'

# Manually fixed addresses
fix_location(233,'US Customs House Chestnut Street Philadelphia PA')
time.sleep(.2)
fix_location(43444, '431 South Streeet Philadelphia PA')
time.sleep(.2)
fix_location(45162, '2457 Grant Ave Philadelphia PA 19114')
time.sleep(.2)
fix_location(69585, '2400 Strawberry Mansion Drive Philadelphia, PA 19132')
time.sleep(.2)
fix_location(44218, 'Chickie and Petes Roosevelt Boulevard, Philadelphia, PA 19116')
time.sleep(.2)
fix_location(48788, 'Diamond Club at Mitten Hall 1913 North Broad Street Philadelphia, PA 19122')
time.sleep(.2)
fix_location(64349, '51 North 12th Street Philadelphia, PA 19107')
time.sleep(.2)
fix_location(64754, '1420 Locust Street Philadelphia PA 19102')
time.sleep(.2)
fix_location(50302, '39 Snyder Ave Philadelphia PA 19148')
time.sleep(.2)
fix_location(61215, '9910 Frankford Ave Philadelphia PA 19114')
time.sleep(.2)
fix_location(65590, '11000 E Roosevelt BLVD Philadelphia PA')
time.sleep(.2)
fix_location(26715, 'Knights Road Shopping Center 4018 Woodhaven Road Philadelphia, PA 19154')
time.sleep(.2)
fix_location(66741, '9183 Roosevelt BLVD Philadelphia PA 19114')
time.sleep(.2)
fix_location(65221, '129 S 30th St Philadelphia PA 19104')
time.sleep(.2)
fix_location(23775, 'The Bellevue Philadelphia PA 19103')
time.sleep(.2)
fix_location(55796, '5765 Wister St Philadelphia PA 19138')
time.sleep(.2)
fix_location(25469, 'Market East Philadelphia PA 19107')
time.sleep(.2)
fix_location(1140, 'torresdale and decatour, philadelphia pa')


