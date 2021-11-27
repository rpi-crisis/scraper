#!/usr/bin/env python3

'''TODO in general:
Account for possibly missing data/fields better
Add course descriptions to the map form the first search results if there is a link
'''

import requests as rq
from bs4 import BeautifulSoup as bs
import json
import re
import time

# Do you want to output the time it took for the operations to complete
timeit = True

# Do you want to output verbose debug information to the console?
debug = True

# Do you want to do a short sample search of only the CSCI courses to test functionality?
# output will be redirected to 'sis_courses_TEST.json' if True
small_search = False

output_file = 'sis_courses_TEST.json' if small_search else 'sis_courses_data.json'

host = "https://sis.rpi.edu"
url_pre = '/rss/bwckctlg.p_display_courses?term_in='
url_post ='&sel_crse_strt=0&sel_crse_end=9999&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr='

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_semester_id(year, part):
    return str(year) + str({
        'spring': '01',
        'arch':   '05',
        'fall':   '09'
    }.get(part))


def course_parts(course_string):
    return course_string[:4], int(course_string[5:9]), course_string[12:]


def fetch_course_links(year, term):
    with rq.Session() as s:
        departments = []
        url = host + url_pre + get_semester_id(year, term) + url_post

        # Go to the search page and get the possible requested departments
        req = rq.get(url, headers=header)
        print("Got search page: " + str(req.status_code))
        search_page = bs(req.text, 'html.parser')
        unparsed_deps = search_page.find('select', {"name": "sel_subj"}).findAll('option', recursive=False)
        for department_option in unparsed_deps:
            departments.append(department_option['value'])

        # Send a request for all of each department's courses
        # If it is a small search, only send the request for the CSCI courses
        req = s.post(url, data={'sel_subj': "CSCI" if small_search else departments}, headers=header)
        print("Got search results: " + str(req.status_code))

        # clean_html = bs(req.text, features="html5lib").prettify() # good looking html for debugging
        #                          Cleans the HTML⤵     will break without this
        search_results = bs(req.text, features='html5lib')
        data = search_results.find('table', {'class': 'datadisplaytable'})
        class_titles = data.find_all(class_='nttitle')
        class_infos = data.find_all(class_='ntdefault')
        for class_title, class_info in zip(class_titles, class_infos):
            soup = bs(class_info.text, features="html5lib")
            desc = soup.find("td").contents[0].strip()
        
        # TODO get the course "description" which includes the prereqs and coreqs and credits from the class_info
        # maybe have an array with the link and parsed description dictionary in it?
        # TODO make a method to parse a description into a dictionary for this
        classes_links_dict = {class_title.a.text: host+class_info.a['href'] for
                              class_title, class_info in zip(class_titles, class_infos)
                              if class_info.a}
        return classes_links_dict


def fetch_section_availability(link):
    with rq.Session() as s:
        req = s.get(link, headers=header)
        section_info = bs(req.text, features='html5lib')
        outer_table = section_info
        if outer_table:
            outer_table = outer_table.find('table', {'class': 'datadisplaytable'})
        else:
            if debug:
                print(f'Unable to read sections at {link}, assuming that it is not being offered currently')
            return None
        inner_table = outer_table.find('table', {'class': 'datadisplaytable'}).find('tbody')

        # Only select the seats information, not the header or waitlist information
        seats = inner_table.find_all('tr')[1].find_all('td')
        return seats[0].text, seats[1].text, seats[2].text


def fetch_course_info(link):
    with rq.Session() as s:
        req = s.get(link, headers=header)
        course_info = bs(req.text, features='html5lib')
        data = course_info.find('table', {'class': 'datadisplaytable'})
        if data:
            data = data.find('tbody').findChildren('tr', recursive=False)
        else:
            if debug:
                print(f'Unable to read course info at {link}, assuming that it is not being offered currently')
            return None
        sections = []

        # For every course section
        for head, info in zip(data[::2], data[1::2]):
            section_info = ""
            if head.a:
                section_info = head.a.text
            else:
                if debug:
                    print(f'Unable to read section info at {link}, assuming that it is not being offered currently')
                return None
            crn = section_info.split('-')[1].strip()
            section = section_info.split('-')[3].strip()

            availability = fetch_section_availability(host + head.a['href'])
            if not availability:
                if debug:
                    print(f'Unable to read section availability at {link}, assuming that it is not being offered currently')
                continue

            meets = info.find('table', {'class': 'datadisplaytable'})
            if meets:
                meets = meets.find('tbody').findChildren('tr', recursive=False)
            else:
                if debug:
                    print(f'Unable to read meeting times from {link}')
                continue
            meets_data = []
            # remove information row
            meets.pop(0)
            for meet in meets:
                parts = meet.findChildren('td', recursive=False)
                instructors = re.sub(' +', ' ', parts[6].text.replace(' (P)', '').strip())
                if instructors == 'TBA' and len(meets_data) > 0:
                    instructors = meets_data[0]['instructors']
                meets_data.append({
                    'time': parts[1].text,
                    'days': parts[2].text,
                    'location': parts[3].text,
                    'type': parts[5].text,
                    'instructors': instructors
                })
            sections.append({
                'crn': crn,
                'section': section,
                'meetings': meets_data,
                'capacity': int(availability[0]),
                'enrolled': int(availability[1]),
                'remaining': int(availability[2])

            })

        if debug:
            for c in sections:
                print(f'CRN:{c["crn"]} - Section:{c["section"]} - {c["enrolled"]}/{c["capacity"]}: {c["remaining"]} left')
                for meet in c['meetings']:
                    print(f'\t{meet["time"]} - {meet["days"]} - {meet["location"]} - {meet["type"]} - {meet["instructors"]}')
        return sections


if __name__ == "__main__":
    before = time.time()
    links = fetch_course_links(2021, "fall")
    if timeit:
        print(f'Took {time.time() - before} to receive initial request for all courses')

    # to use this in general you would go through the value items of the links dictionary
    # and call fetch_course_info on each value
    store = []

    before = time.time()
    i = 0
    size = len(links)
    for link in links.values():
        if debug:
            print(f'{i}/{size}')
        else:
            print('*', end='')
            if i % 50 == 49:
                print('')
        store.append(fetch_course_info(link))
        i += 1
    if timeit:
        print(f'\nTook {time.time() - before} to go to all sublinks')
    print(f'outputting into {output_file}')
    json.dump(store, open(output_file, 'w'))
