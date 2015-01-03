from bs4 import BeautifulSoup
import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE1 = os.path.join(PROJECT_ROOT, 'dbs', 'licensees.db')

conn = sqlite3.connect(DATABASE1)
c = conn.cursor()

try:
	c.execute('DROP TABLE licensees')
	c.execute('DROP TABLE cases')
finally:
	c.execute('''CREATE TABLE licensees (lid INT PRIMARY KEY NOT NULL UNIQUE, 
										 name TEXT, 
										 address TEXT, 
										 zipcode INT,
										 trade_name TEXT, 
										 license_no TEXT, 
										 license_type TEXT, 
										 license_type_title TEXT,
										 license_type_code TEXT,
										 status TEXT, 
										 tavern_gaming_status TEXT, 
										 original_owner TEXT, 
										 current_owner TEXT)''')
	c.execute('PRAGMA foreign_keys = ON')
	c.execute('''CREATE TABLE cases  (case_id INTEGER PRIMARY KEY,
									  lid INT NOT NULL,
									  penalty TEXT, 
									  penalty_text TEXT,
									  fine INT,
									  initiation_date TEXT, 
									  FOREIGN KEY(lid) REFERENCES licensees(lid))''')

fileroot = 'saved_html/licensee_source_'
filetail = '.html'

for x in range(114):

	filenum = str(x+1).zfill(4)

	filename = fileroot + filenum + filetail

	print filename

	page = open(filename)
	soup = BeautifulSoup(page,'html.parser')
	page.close()


	main_content = soup.find(id="MainContent_UpdatePanel1").find("tbody")

	rows = main_content.find_all('tr')

	print 'Number of rows:'
	print len(rows)

	headercount = 0
	locator = None

	rowcount = 0


	for row in rows:
		rowcount+=1
		attributes = row.attrs
		
		if 'style' in attributes: #Identify headers of licensee
			
			locatorrow = rowcount
			if attributes['style'] == 'background-color:#800000': #Identify licensee
				general_info={}
				cases = []
				casenum = 0
				headercount+=1
				locator = row.find('font').text
			else: #Identifies sub-header of licensee
				locator = row.find(class_='heading').text

		if (locator == 'GENERAL LICENSEE INFORMATION' or locator == 'OWNER ISSUE DATES') and rowcount != locatorrow:
			cells = row.find_all('td')
			for cell in cells:
				heading_title = cell.find(class_="fieldHeading")
				the_data = cell.find(class_="data")
				if heading_title and the_data:
					if heading_title.text[:-1] == 'Address':
						contents = the_data.contents
						contents = [x for x in contents if x.string != None]
						general_info[heading_title.text[:-1]] = " ".join(contents)
						general_info['Zipcode'] = int(contents[-1][0:5])
					elif heading_title.text[:-1] == 'License Type':
						contents = the_data.text.split('-')
						license_type_title = "-".join(contents[0:-1]).strip()
						license_type_code = contents[-1].strip()[1:-1].strip()
						general_info['License Type Title'] = license_type_title
						general_info['License Type Code'] = license_type_code
						general_info[heading_title.text[:-1]] = the_data.text
					else:
						general_info[heading_title.text[:-1]] = the_data.text

		if locator == 'CITATION CASE INFORMATION(Click on the Case Number(s) for Citation detail)' and rowcount != locatorrow:
			cells = row.find_all('td')
			for cell in cells:
				heading_title = cell.find(class_="fieldHeading").text[:-1]
				if heading_title == 'Penalty':
					penalty = cell.find(class_="data").text
					penalty_split = penalty.split('-')
					penalty_text = " ".join(penalty_split[0:-1]).strip()
					if len(penalty_split) > 1:
						fine = int(penalty_split[-1].strip()[2:-4])
					else:
						fine = None

				if heading_title == 'Initiation Date':
					initiation_date = cell.find(class_="data").text
					cases.append({'penalty':penalty, 'penalty_text':penalty_text, 'fine':fine, 'initiation_date':initiation_date})
					penalty = None
					initiation_date = None

		if locator == 'APPLICATION CASE INFORMATION' and rowcount == locatorrow:
			c.execute('''INSERT INTO licensees (lid, name, address, zipcode, trade_name, license_no, 
												license_type, license_type_title, license_type_code, status, tavern_gaming_status,
												original_owner, current_owner)
												VALUES
												(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
												[general_info['LID'], general_info['Name'],
												general_info['Address'], general_info['Zipcode'],
												general_info['Trade Name'], general_info['License No'], 
												general_info['License Type'], 
												general_info['License Type Title'],
												general_info['License Type Code'],
												general_info['Status'], 
												general_info['Tavern Gaming Status'],
												general_info['Original Owner'], 
												general_info['Current Owner']])
			if cases:
				for case in cases:
					c.execute('''INSERT INTO cases (lid, penalty, penalty_text, fine, initiation_date) VALUES (?, ?, ?, ?, ?)''',
						[general_info['LID'], case['penalty'], case['penalty_text'], case['fine'],case['initiation_date']])



	print 'HeaderCount'
	print headercount

conn.commit()
c.close()
