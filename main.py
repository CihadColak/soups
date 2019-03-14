import requests
import collections
from bs4 import BeautifulSoup

pages = []

baseurl = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/an'

# Cycle through all Uppercase letters
for i in range(65,91):
	letter = chr(i)
	j= 1

	# Cycle through all pages 
	while(True):
	    url = baseurl + letter + str(j) + '.htm'
	    print(url)
	    page_request = requests.get(url)
	    
	    # End on 404
	    if page_request.status_code == 404:
	        break
	        
	    pages.append(page_request)
	    j += 1

# Initialize lists for later usage
infos,countries,lifetime_list = ([],[],[])

# Cycle through every pageurl we gathered earlier and look for nationality and additional information
for page in pages:
    pageindex = 1
    
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    # Pull all text from the bodytext div, find.table filters all empty and irrelevant lines
    artist_name_list = soup.find(class_='BodyText').find('table')


    # Pull text from all Instances of <a> tag within bodytext div
    artist_name_list_items = artist_name_list.find_all('a')
    
    # Cycle through every artist
    for tr in artist_name_list.find_all('tr'):
        val = tr.find_all("td")[1].text
        if not val == "":
            infos.append(val)

            try:
            	country, lifetime  = val.split(', ')
            	print("added" + country)
            except ValueError:
            	print(pageindex, val)
            	continue
            
            countries.append(country)
            lifetime_list.append(lifetime)
    pageindex += 1

country_counter = collections.Counter(countries)

print(country_counter)

