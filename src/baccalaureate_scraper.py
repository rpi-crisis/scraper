from cgi import test
from bs4 import BeautifulSoup
from numpy import equal
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
    "years": [[], [], [], [], []], 
    "other-content": {}}
    baccalaureate[major_title]["other-content"] = {"options": " ", "capstone": " ", "transfer_policy": " ", "footnotes": " ", "misc": " "}
    
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
    
    if yearsHTML == None:
        continue 
    yearlist = yearsHTML.find("div", class_ = "acalog-core")
    count = 0
    yearcount = 0
    #print(yearsHTML)
    #print("---------------------------")
    while(yearlist != None):
        #print(yearlist)
        if (count > 3 and major_title != "Architecture") or (count > 4 and major_title == "Architecture"):
            try:
                testString = yearlist.h2.a
                #print(testString)
                if "Footnotes" in testString:
                    baccalaureate[major_title]["other_content"]["footnotes"].append(yearlist)
                elif "Capstone" in testString:
                    baccalaureate[major_title]["other_content"]["capstone"].append(yearlist)
                elif "Transfer Credit Policy" in testString:
                    baccalaureate[major_title]["other_content"]["transfer_policy"].append(yearlist)
                elif "Options" in testString:
                    baccalaureate[major_title]["other_content"]["options"].append(yearlist)
                else:
                    baccalaureate[major_title]["other_content"]["misc"].append(yearlist)
            except:
                continue
        else:
            baccalaureate[major_title]["years"][count].append(yearlist)
        yearlist = yearlist.next_sibling
        yearcount += 1
        if yearcount > 1:
            yearcount = 0
            count += 1
        #print("-------")
    
    #print(baccalaureate[major_title]["years"])
    #print("----------------------")