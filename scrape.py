from selenium import webdriver
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH, options=op)

url = "http://catalog.rpi.edu/content.php?catoid=22&navoid=542"

driver.get(url)

source_first = driver.page_source
soup_first = BeautifulSoup(source_first, "html.parser")

# the data is arranged in a table of ul elements
# the first ul element is the list of baccalaureate programs

table = soup_first.find('ul', {'class': 'program-list'})

# find all the list items in the ul
table_li = table.find_all("li")

program_names = []
program_links = []
for li in table_li: #grab the text and the link in the li element
    program_names.append(li.find('a').text.strip()) # must strip trailing spaces
    program_links.append(li.find('a')['href'])

dictionary = {} #our json object
bug_programs = ["Physician-Scientist", "Program for Graduates of Naval Nuclear Power Training Command’s Nuclear Power School"]
for program in program_names:
    #print(program)
    
    if program not in bug_programs:
        i = 1
        years = {}
        driver.find_element_by_link_text(program).click()
        #now we are in the link for each program
        source_link = driver.page_source
        soup_link = BeautifulSoup(source_link, "html.parser")

        #print(soup_link.find_all())
        #there are two tables in the html, we need to find the second one
        td = soup_link.find('td', {'class': 'block_content'})
        table = td.find('table', {'class': 'table_default'})
        tbody = table.find('tbody')
        #we need to get the second table row, first one is a header
        tr = tbody.find_all('tr')[3]
        print(len(tr))
        #tr = tr[1]; # the second tr
        #there is one td in the tr that holds all the data
        #analog core class is the year
        #custom leftpad 20 has the contents of the of that year
        #within the leftpad20 class are two analog core classes that have each semester
        td_new = tr.find('td', {'colspan': '4'})
        if (not td_new):
            tr = tbody.find_all('tr')[4]
            td_new = tr.find('td', {'colspan': '4'})
        
        div = td_new.find('div', class_='custom_leftpad_20')
        leftpad20 = div.find_all('div', class_='custom_leftpad_20')[:4]#first 4 years, can be adjusted
        
        for term in leftpad20:
            
            terms_dict = {}
            #there will be two analog core
            analog_core = term.find_all('div', class_='acalog-core') #there should be 2, fall and spring
            
            #print(year_num)
            for sem in analog_core:
                year_num = str(i)
                term_text = ""
                if sem.find('h3'):
                    term_text = sem.find('h3').text #fall or spring
                #print(sem.find('h3').text)
                #within the analog core there are two ul
                ul = sem.find_all('ul')
                #the first ul has all the non hyperlinked classes ex: hass elective or free elective or math option
                nonlinked = ul[0]
                nonlinked_text = []
                li = nonlinked.find_all('li')
                for l in li:
                    nonlinked_text.append(l.text)
                terms_dict[term_text]= []
                ##terms_dict[term_text].append(nonlinked_text)
                linked_text = [] 
                if(len(ul) > 1):
                    linked = ul[1]
                    li_linked = linked.find_all('li')
                    for l in li_linked:
                        linked_text.append(l.text)
                all_classes = []
                for l in nonlinked_text:
                    all_classes.append(l)
                for l in linked_text:
                    all_classes.append(l)
                for k in range(len(all_classes)):
                    all_classes[k] = all_classes[k].replace("\u00a0", " ")
                    all_classes[k] = all_classes[k].replace("\n\t", " ")
                    l = [char for char in all_classes[k] if char.isalnum() or char == " " or char == "-" or char == ":" or char == ","]
                    all_classes[k] = "".join(l)
                terms_dict[term_text].append(all_classes)
                #print(all_classes)
                    ##terms_dict[term_text].append(linked_text)
            years[year_num] = terms_dict
            i+=1
        dictionary[program] = years
                        #the second ul has all the required classes hyperlinked
        driver.back()
driver.close()
#print(dictionary)
        #driver.close()
json_obj = json.dumps(dictionary, indent=4)
with open("sample.json", "w") as outfile:
    outfile.write(json_obj)



