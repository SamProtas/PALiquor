from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

browser = webdriver.Firefox() #PhantomJS page_source is incorrect. Maybe due to fast loading speed caused by headless browser?

browser.get('https://www.lcbapps.lcb.state.pa.us/webapp/PublicLicenseeSearch/LicenseeSearch.aspx')

content = browser.page_source

license_status = Select(browser.find_element_by_name("ctl00$MainContent$ddlLicenseStatus"))
license_status.select_by_value("X")

time.sleep(2)

municipality = Select(browser.find_element_by_name("ctl00$MainContent$ddlMunicipality"))
municipality.select_by_value("51005-PHILADELPHIA")

time.sleep(2)

browser.find_element_by_name("ctl00$MainContent$btnSearch").click()

time.sleep(3)


page_status = browser.find_element_by_id("MainContent_lblCurrentPage").text
current_page = page_status.split()[0]
total_pages_master = page_status.split()[-1]

print 'Current Page:'
print current_page
print 'Total Pages:'
print total_pages_master

fileroot = 'saved_html/'
filename = fileroot + 'licensee_source_0001.html'
html_file = open(filename,'w')
html_file.write(browser.page_source.encode('utf8'))
html_file.close()

for page in range(2,int(total_pages_master)+1):
	print 'Page to load:'
	print page

	browser.find_element_by_id("MainContent_cmdNext").click()

	time.sleep(2)

	page_status = browser.find_element_by_id("MainContent_lblCurrentPage").text
	current_page = page_status.split()[0]
	total_pages = page_status.split()[-1]

	print 'Current Page:'
	print current_page
	print 'Total Pages:'
	print total_pages

	filename = fileroot + 'licensee_source_' + current_page.zfill(4) + '.html'
	html_file = open(filename,'w')
	html_file.write(browser.page_source.encode('utf8'))
	html_file.close()

