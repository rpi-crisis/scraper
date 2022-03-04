from tracemalloc import start
from bs4 import BeautifulSoup
import requests
r = requests.get("http://catalog.rpi.edu/content.php?catoid=22&navoid=542")
baccalaureate = {}
soup = BeautifulSoup(r.content, 'html5lib')
table = soup.find("td", class_="block_content")
major_elements = table.find_all("ul", class_="program-list")
ba_elements = major_elements[0].find_all("a")
for z in ba_elements:
    major_title = z.text.strip()
    major_link = z.get('href')
    baccalaureate[major_title] = {"description": " ", "requirements": " ", 
    "years": [[], [], [], []], 
    "other-content": {}}
    baccalaureate[major_title]["other-content"] = {"options": " ", "capstone": " ", "transfer_policy": " ", "footnotes": " "}
    major_webpage = requests.get("http://catalog.rpi.edu/" + major_link)
    major_soup = BeautifulSoup(major_webpage.content, 'html5lib')
    major_table = major_soup.find("td", class_="block_content")
    major_table_def = major_table.find("table", class_="table_default")
    trs = major_table_def.find_all("tr")
    description_tr = trs[0]
    requirement_tr = trs[3]
    baccalaureate[major_title]["description"] = description_tr
    baccalaureate[major_title]["requirements"] = requirement_tr   
    yearsHTML = requirement_tr.find("div", class_="custom_leftpad_20")
    yeartitlelist = yearsHTML.find_all("div", class_ = "acalog-core")
    yeardescriptionlist = yearsHTML.find_all("div", class_="custom_leftpad_20")
    for x in range(0, len(yeartitlelist)):
        baccalaureate[major_title]["years"][x].add(yeartitlelist[x])
        baccalaureate[major_title]["years"][x].add(yeardescriptionlist[x])
    
    print("----------------------")
    break
