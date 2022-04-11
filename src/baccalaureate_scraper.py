from bs4 import BeautifulSoup
import requests
import time
import re

def baccalurate_grab_html():
    r = requests.get("http://catalog.rpi.edu/content.php?catoid=22&navoid=542")
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find("td", class_="block_content")
    major_elements = table.find_all("ul", class_="program-list")
    ba_elements = major_elements[0].find_all("a")

    for z in ba_elements:
        #grabbing major title as well as the link to the major page
        major_title = z.text.strip()
        major_link = z.get('href')
        
        #defining the inner values of the mega dictionaries
        baccalaureate_parsed[major_title] = {"description": [], 
        "years": [[], [], [], [], []], 
        "other-content": {}}
        baccalaureate_parsed[major_title]["other-content"] = {"options": " ", "capstone": " ", "transfer_policy": " ", "footnotes": [], "misc": []}

        baccalaureate[major_title] = {"description": " ", "requirements": " ", 
        "years": [[], [], [], [], []], 
        "other-content": {}}
        baccalaureate[major_title]["other-content"] = {"options": " ", "capstone": " ", "transfer_policy": " ", "footnotes": " ", "misc": []}
        
        #getting the HTML from the webpage for the individual major
        major_webpage = requests.get("http://catalog.rpi.edu/" + major_link)
        major_soup = BeautifulSoup(major_webpage.content, 'html5lib')

        #parsing through the large HTML from the webpage in order to  get the description of the major as well as the massive list of requirements
        major_table = major_soup.find("td", class_="block_content")
        major_table_def = major_table.find("table", class_="table_default")
        trs = major_table_def.find_all("tr")
        description_tr = trs[0]
        #print(description_tr.get_text())
        #print(description_tr.get_text().find("Return to: Programs"))
        #print(description_tr.get_text()[description_tr.get_text().find("Return to: Programs") + 19])
        if description_tr.get_text()[description_tr.get_text().find("Return to: Programs") + 19].isalpha():
            description_tr = description_tr
        else:
            description_tr = "NO DESCRIPTION"
        #print(description_tr)
        #print("-------------------------------")
        if major_title == "Architecture":
            requirement_tr = trs[4]
        else:
            requirement_tr = trs[3]
        baccalaureate[major_title]["description"] = description_tr
        baccalaureate[major_title]["requirements"] = requirement_tr  
        
        #yearHTML is all of the raw description HTML for the entire major.
        yearsHTML = requirement_tr.find("div", class_="custom_leftpad_20")
        if yearsHTML == None:
            continue 

        #yearHTML will be used to get the raw HTML for each year.
        yearlist = yearsHTML.find("div", class_ = "acalog-core")
        
        #count and yearcount will be used to  put the raw HTML in each value of the years array.
        count = 0
        yearcount = 0

        #if there are no more HTML chunks, then the loop ends
        while(yearlist != None):
            #debug print
            #print(yearlist.h2.a['name'])
            #print(major_title)

            #for SOME reason, ITWS has an extensive amount of major information that needs to be parsed before getting to
            #each major year, I have to add extra lists to add the HTML information to the mega dictionary.
            if major_title == "Information Technology and Web Science" and len(baccalaureate[major_title]["years"]) == 5:
                print("CHECKED!!!")
                for g in range(6):
                    baccalaureate[major_title]["years"].append([])
                for g in range(4, 11):
                    baccalaureate[major_title]["years"][g].append(yearlist)
                    yearlist = yearlist.next_sibling
                    baccalaureate[major_title]["years"][g].append(yearlist)
                yearlist = yearlist.next_sibling
                
            


            #checks to see if there are any extra bits of HTML after getting through the inital 4/5 years.
            if (count > 3 and major_title != "Architecture") or (count > 4 and major_title == "Architecture"):
                try:
                    #debug print
                    #print(yearlist)
                    testString = yearlist.h2.a['name']

                    #checks to see if they fall into a specific category that we defined in the mega dictionary
                    if "Footnotes" in testString:
                        baccalaureate[major_title]["other-content"]["footnotes"] = yearlist
                    elif "Capstone" in testString:
                        baccalaureate[major_title]["other-content"]["capstone"] = yearlist
                    elif "Transfer Credit Policy" in testString:
                        baccalaureate[major_title]["other-content"]["transfer_policy"] = yearlist
                    elif "Options" in testString:
                        baccalaureate[major_title]["other-content"]["options"] = yearlist
                    else:
                        baccalaureate[major_title]["other-content"]["misc"].append(yearlist)
                except Exception as e:
                    #print(e)
                    baccalaureate[major_title]["other-content"]["misc"].append(yearlist)
            else:
                baccalaureate[major_title]["years"][count].append(yearlist)
                yearcount += 1
                if yearcount > 1:
                    yearcount = 0
                    count += 1
            
            #switches to the next HTML chunk
            yearlist = yearlist.next_sibling
            
            #yearcount increases by 1 until it is 2. If it's greater than 2, yearcount goes to 0 and count increases by 1.
            #this is to ensure that each year gets not only the title HTML, but the information for that year as well.
            

def baccalurate_parse_html():
    for x in baccalaureate:
        #print(x)
        #print("------------------------")
        #print(baccalaureate[x]["description"])
        if baccalaureate[x]["description"] != "NO DESCRIPTION":
            for y in baccalaureate[x]["description"].find_all("p"):
                if y.get_text() != " Return to: Programs":
                    inserted_string = y.get_text().replace("\xa0", "")
                    inserted_string = inserted_string.replace("\n", "")
                    inserted_string = inserted_string.replace("\t", "")
                    baccalaureate_parsed[x]["description"].append(inserted_string)
        yearcounter = 0
        for y in baccalaureate[x]["years"]:
            try:
                #print(y)
                #print(y[0].h2.a["name"])
                baccalaureate_parsed[x]["years"][yearcounter] = []
                baccalaureate_parsed[x]["years"][yearcounter].append(y[0].h2.a["name"])
                baccalaureate_parsed[x]["years"][yearcounter].append([])
                baccalaureate_parsed[x]["years"][yearcounter].append([])
                #print(baccalaureate_parsed[x]["years"])
                #print("------------------------------------------------")
                #baccalaureate_parsed[x]["years"][1] = []
                yearlist = y[1].find_all("div")
                for z in yearlist:
                    #print(z.find_all("li"))
                    for i in z.find_all("li"):
                        #print(i.get_text())
                        if "or" == i.get_text():
                            continue
                        else:
                            inserted_string = i.get_text().replace("\xa0", "")
                            inserted_string = inserted_string.replace("\n", "")
                            inserted_string = inserted_string.replace("\t", "")
                            footnote_value = " "
                            footnote_found = False
                            credit_hour_found = False
                            credit_hour_value = ""
                            if "(See footnote" in inserted_string:
                                #print(inserted_string.index("(See footnote "))
                                footnote_value = inserted_string[inserted_string.index("(See footnote ") + 14]
                                inserted_string = inserted_string.replace("(See footnote " + footnote_value + " below)", "")
                                footnote_found = True
                            
                            if "Credit Hours" in inserted_string:
                                #print(inserted_string.index("Credit Hours: "))
                                credit_hour_value = inserted_string[inserted_string.index("Credit Hours: ") + 14]
                                #print(credit_hour_value)
                                inserted_string = inserted_string.replace("Credit Hours: " + credit_hour_value, "")
                                credit_hour_found = True  
                            
                            if footnote_found == True:
                                inserted_string = inserted_string + "[FOOTNOTE: " + footnote_value + "]"
                            if credit_hour_found == True:
                                inserted_string = inserted_string + " [CREDIT HOURS: " + credit_hour_value + "]"
                            if "Fall" in z.h3.a["name"]:
                                baccalaureate_parsed[x]["years"][yearcounter][1].append(inserted_string)
                            if "Spring" in z.h3.a["name"]:
                                baccalaureate_parsed[x]["years"][yearcounter][2].append(inserted_string)
                        #print("-----------------------")
                
                #print("------------------------------------------------")
                yearcounter += 1
            except Exception as e:
                #print(e)
                #print("------------------------------------------------")
                continue
        #print("------------------")
        for y in baccalaureate[x]["other-content"]:
            if len(baccalaureate[x]["other-content"][y]) == 0 or baccalaureate[x]["other-content"][y] == " ":
                print("NO CONTENT HERE")
            else:
                #print(y)
                #print("---------------------------------")
                #print(baccalaureate[x]["other-content"][y])
                try:
                    li_list = baccalaureate[x]["other-content"][y].find_all("li");
                    for z in li_list:
                        #print(z.get_text())
                        inserted_string = z.get_text().replace("\xa0", "")
                        inserted_string = inserted_string.replace("\n", "")
                        inserted_string = inserted_string.replace("\t", "")
                        baccalaureate_parsed[x]["other-content"][y].append(inserted_string)
                except Exception as e:
                    #print(baccalaureate[x]["other-content"][y])
                    print(e)
                #print(li_list)
            #print("--------------------")
        

#printing all the information in the mass dictionary (DEBUG)
time_start = time.time()
baccalaureate = {}
baccalaureate_parsed = {}
baccalurate_grab_html()
baccalurate_parse_html()

print(baccalaureate["Information Technology and Web Science"]["years"])
print("-------------------------------------")
print(baccalaureate_parsed["Information Technology and Web Science"])
#for x in baccalaureate_parsed:
#    print(x)
#    print("----------")
#    print(baccalaureate_parsed[x])
#    print("-------------------------------------------------")

#runtime (DEBUG)
print(time.time() - time_start)