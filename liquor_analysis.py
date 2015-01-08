import os
import pandas as pd
import numpy as np 
import sqlite3
import shapefile as sf
import matplotlib.patches as patches
import matplotlib.pyplot as plt

pd.set_option('display.mpl_style', 'default')
figsize(15, 5)

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE1 = os.path.join(PROJECT_ROOT, 'dbs', 'licensees.db')
DATABASE2 = os.path.join(PROJECT_ROOT, 'dbs', 'liquorstores.db')
DATABASE3 = os.path.join(PROJECT_ROOT, 'dbs', 'zipatlas_populations.csv')

conn1 = sqlite3.connect(DATABASE1)
conn2 = sqlite3.connect(DATABASE2)


df_licensees = pd.read_sql('SELECT * FROM licensees', conn1, parse_dates=[
    'current_owner', 'original_owner'])
df_cases = pd.read_sql('SELECT * FROM cases', conn1)
df_state_stores = pd.read_sql('SELECT * FROM liquorstores', conn2)
df_zip_populations = pd.read_csv(DATABASE3, header=0, thousands=',')

license_type_counts = df_licensees['license_type_title'].value_counts()

ax = df_cases['fine'].plot(kind='hist', bins=100, cumulative=True, normed='True')
ax.set_xlabel('Fine ($)')
ax.set_ylabel('Fraction of All Cases')
ax.set_title('Cumulative Histogram of Fines')

liquor_stores_per_zipcode = df_state_stores['zipcode'].value_counts()


philly_map = sf.Reader('maps/tl_2014_42_cousub/tl_2014_42_cousub')
philly_data = philly_map.records()
philly_shapes = philly_map.shapes()

fig = plt.figure(figsize=(11.7,11.7))#8.3))
ax = plt.subplot(111, aspect='equal')

for ii in range(len(philly_data)):
    city = philly_data[ii][6]
    if city[:12] == "Philadelphia":
        location = ii
        
points = philly_shapes[location].points
x,y=zip(*points)
bol=patches.Polygon(points,True)
ax.add_patch(bol)

ax.autoscale()
xlim = ax.get_xlim()
ylim = ax.get_ylim()


#plt.plot(-75.10, 40, 'ro')
latitudes = list(df_state_stores['longitude'])
longitudes = list(df_state_stores['latitude'])

#latitudes2 = list(df_licensees['latitude'])
#longitudes2 = list(df_licensees['longitude'])

latlon = df_licensees[['latitude','longitude']].values
clean_latlong =[]
for jj in latlon:
    if jj[0] > 39.6 and jj[0] < 40.5 and jj[1] > -75.5 and jj[1] < -74.5:
        clean_latlong.append([jj[1],jj[0]])
      
longs2 = [x[0] for x in clean_latlong]
lats2 = [x[1] for x in clean_latlong]      
      
plt.plot(longs2,lats2, 'ro')

#plt.plot(longitudes2, latitudes2, 'ro')
plt.plot(longitudes, latitudes, 'yo')

ax.set_xlim(xlim)
ax.set_ylim(ylim)

plt.show()
