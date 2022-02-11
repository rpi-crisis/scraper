"""
Note: This is currently a work in-progress. The main functionality
works. However, there are some inconsistencies not yet accounted for.

Notice in the HTML of the table on the catalog website, there are some
dates/events in divs as well as ps. In addition, there may be multiple
within a div section.

This portion will need to be resolved before the json is fully functional.
"""


import requests as rq, json
from bs4 import BeautifulSoup as bs

# parse spring and fall data
def parse_table_rows(out, rows):
    date = ""

    for row in rows:
        # make sure row has contents
        if len(row)==0: continue
        # bold means it's a date
        # if (row.findAll("em", recursive=True)): continue
        if (row.findAll("strong", recursive=False)):
            try:
                data = row.text.strip()
                # check if date/information are in same cell
                data = data.split('\r')
                if len(data) == 2:
                    date = data[0].strip()
                    # remove non-printable codes
                    date = date.encode("ascii","ignore")
                    date = date.decode()
                    # check if date already exists
                    if date not in out.keys():
                        out[date] = []
                    # gather the information for given date
                    information = data[1].strip()
                    # remove non-printable codes
                    information = information.encode("ascii","ignore")
                    information = information.decode()
                    # add gathered information to the list at that date
                    out[date].append(information)
                else:
                    # there is not both date/information in the cell
                    date = data[0]
                    if date not in out.keys():
                        out[date] = []
            except:
                continue
        # the text is not bold - this cell contains information about a date
        else:
            data = row.text.strip()
            # remove non-printable codes
            data = data.encode("ascii","ignore")
            data = data.decode()
            if date not in out.keys():
                # there will always be a date before first information
                # the date will be the last cell date if not in same cell
                out[date] = []
            out[date].append(data)

# remove null items from each list
def check_data(out):
    for value in out.keys():
        out[value] = list(filter(('').__ne__, out[value]))


calendar_website = "http://catalog.rpi.edu/content.php?catoid=22&navoid=528"
calendar_html = rq.get(calendar_website).text
soup = bs(calendar_html, "html.parser")

# Find the correct table
tables = soup.find_all("td",{
    "style": "vertical-align:top; width:48%"
}) # get the two tables for fall and spring

# first table found will be fall
table_fall = tables[0]
# second table found will be spring
table_spring = tables[1]

# get data from inside the tables
rows_fall = table_fall.findAll(["p","div"], recursive = False)
rows_spring = table_spring.findAll(["p","div"], recursive = False)

# initialize dictionaries
calendar_fall = {}
calendar_spring = {}

# parse data for fall and spring
parse_table_rows(calendar_fall, rows_fall)
parse_table_rows(calendar_spring, rows_spring)

# check the data before saving
check_data(calendar_fall)
check_data(calendar_spring)

out = open("fall_calendar.json","w")
json.dump(calendar_fall, out)
out.close()

out = open("spring_calendar.json", "w")
json.dump(calendar_spring, out)
out.close()

# for testing purposes
if __name__ == "__main__":
    # print contents of fall calendar
    for date in calendar_fall:
        value = date + ':'
        try: print(value, calendar_fall[date])
        except: continue

    # print contents of spring calendar
    for date in calendar_spring:
        value = date + ':'
        try: print(value, calendar_spring[date])
        except: continue
