from bs4 import BeautifulSoup
import requests
import time
start_time = time.time()
r = requests.get("http://catalog.rpi.edu/content.php?catoid=22&navoid=542")
#print(r.content)

baccalaureate = {}
soup = BeautifulSoup(r.content, 'html5lib')
#print(soup)
table = soup.find("td", class_="block_content")
major_elements = table.find_all("ul", class_="program-list")
ba_elements = major_elements[0].find_all("a")
for z in ba_elements:
    #print(z.text.strip())
    major_title = z.text.strip()
    major_link = z.get('href')
    baccalaureate[major_title] = {"description": " ", "requirements": " "}
    major_webpage = requests.get("http://catalog.rpi.edu/" + major_link)
    major_soup = BeautifulSoup(major_webpage.content, 'html5lib')
    major_table = major_soup.find("table", class_="table_default")
    description_tr = major_table.find("tr")
    requirement_tr = description_tr.find_next("tr")
    baccalaureate[major_title]["description"] = description_tr
    baccalaureate[major_title]["requirements"] = requirement_tr     
print(time.time() - start_time)
