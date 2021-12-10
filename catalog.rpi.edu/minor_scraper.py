from selenium import webdriver
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH,options=op)

url = "http://catalog.rpi.edu/content.php?catoid=22&navoid=542"

driver.get(url)

source_first = driver.page_source
soup_first = BeautifulSoup(source_first, "html.parser")

table = soup_first.find_all('ul', {'class': 'program-list'})[6]
#this is the ul for the pathways

table_li = table.find_all('li')

program_names = []
program_links = []
for li in table_li: #grab the text and the link in the li element
    program_names.append(li.find('a').text.strip()) # must strip trailing spaces
    program_links.append(li.find('a')['href'])

bug_programs = []
dictionary = {}
for i in range(len(program_names)):
    program = program_names[i]
    if program not in bug_programs:
        print(program)
        dictionary[program] = {}
        #click on the link for the minor
        driver.find_element_by_link_text(program).click()

        source_link = driver.page_source
        soup_link = BeautifulSoup(source_link, "html.parser")
        
        table = soup_link.find('table', {'class': 'table_default'})
        #all the categories are stored in acalog core divs
        divs = table.find_all('div', {'class': 'acalog-core'})
        #now we are in the right program

        for div in divs:
            #each div contains a different category of information
            classes = []
            #the div always has text but some dont have h2 tags
            div_text = div.text
            if(div.find('h2')):
                div_text = div.find('h2').text
            #parse the div string
            div_text = div_text.replace('\ua00a0', '')
            div_text = div_text.replace('\u200b', '')
            div_text = div_text.replace('\n', '')
            div_text = div_text.replace('\u2013', '')
            #find the list of classes
            class_list = div.find('ul')
            if(class_list): #the list exists
                for li in class_list.find_all('li'):
                    #parse the string
                    text = li.text
                    text = text.replace('\u00a0', '')
                    text = text.replace('\u2013', ' -')
                    text = text.replace('\n', '')
                    if text != "":
                        classes.append(text)
            elif(len(div.find_all('p')) > 0):
                #if theres no list than theres a paragraph
                p_list = div.find_all('p')
                for p in p_list:
                    #parse the paragraph
                    text = p.text
                    text = text.replace('\u00a0', '')
                    text = text.replace('\u200b', '')
                    text = text.replace('\n', '')
                    if text != "":
                        classes.append(text)
            elif(div.find('ol')): #there could be an ordered list
                o_list = div.find('ol')
                for li in o_list.find_all('li'):
                    text = li.text
                    text = text.replace('\u00a0', '')
                    text = text.replace('\u2013', ' -')
                    text = text.replace('\n', '')
                    classes.append(text)
            if(len(classes) > 0):
                dictionary[program][div_text] = classes
        if(len(divs) == 0): #some minors do not have any divs and are just text
            #we need to move to the right table
            tables = soup_link.find_all('table', {'class': 'table_default'})
            table = tables[len(tables)-2]
            classes = []
            p_list = table.find_all('p')
            ul = table.find('ul')
            if(p_list) : 
                for p in p_list:
                    text = p.text
                    text = text.replace('\u00a0', '')
                    text = text.replace('\u200b', '')
                    text = text.replace('\n', '')
                    classes.append(text)
            if(ul):
                for li in ul.find_all('li'):
                    text = li.text
                    text = text.replace('\u00a0', '')
                    text = text.replace('\u2013', ' -')
                    text = text.replace('\n', '')
                    classes.append("- " + text)
            if (len(classes) > 0):
                dictionary[program]["Information"] = classes[1:]
        driver.back()

json_obj = json.dumps(dictionary, indent=4)
with open("minors.json", "w") as outfile:
    outfile.write(json_obj)
driver.close()