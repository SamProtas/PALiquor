import os
import pandas as pd
import numpy as np 
import sqlite3

pd.set_option('display.mpl_style', 'default')
figsize(15, 5)

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE1 = os.path.join(PROJECT_ROOT, 'dbs', 'licensees.db')
DATABASE2 = os.path.join(PROJECT_ROOT, 'dbs', 'liquorstores.db')

conn1 = sqlite3.connect(DATABASE1)
conn2 = sqlite3.connect(DATABASE2)


df_licensees = pd.read_sql('SELECT * FROM licensees', conn1, parse_dates=[
    'current_owner', 'original_owner'])
df_cases = pd.read_sql('SELECT * FROM cases', conn1)
df_state_stores = pd.read_sql('SELECT * FROM liquorstores', conn2)

license_type_counts = df_licensees['license_type_title'].value_counts()

ax = df_cases['fine'].plot(kind='hist', bins=100, cumulative=True, normed='True')
ax.set_xlabel('Fine ($)')
ax.set_ylabel('Fraction of All Cases')
ax.set_title('Cumulative Histogram of Fines')

