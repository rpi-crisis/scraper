"""
Searches and scrapes course information for SIS
without requiring login / two-factor authentication.

A JSON file is generated with additional course information.
"""

import requests as rq, json
from bs4 import BeautifulSoup as bs

headerss = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

search_data = {
        'term_in': '202101',
        'call_proc_in': '',
        'sel_subj': 'dummy',
        'sel_levl': 'dummy',
        'sel_schd': 'dummy',
        'sel_coll': 'dummy',
        'sel_divs': 'dummy',
        'sel_dept': 'dummy',
        'sel_attr': 'dummy',
        'sel_subj': 'ADMN',
        'sel_crse_strt': '',
        'sel_crse_end': '',
        'sel_title': '',
        'sel_levl': '%',
        'sel_schd': '%',
        'sel_coll': '%',
        'sel_divs': '%',
        'sel_dept': '%',
        'sel_from_cred': '',
        'sel_to_cred': '',
        'sel_attr': '%'
}

# accesses each search correctly
# still needs to obtain data from each search
with rq.Session() as s:
        url = 'https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in=202101&sel_crse_strt=0&sel_crse_end=9999&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr='
        r = rq.get(url, headers=headerss)
        soup = bs(r.text, 'html.parser')
        value = soup.find('select', {"name": "sel_subj"})
        value = value.findAll('option', recursive = False)

        courses = {}
        searches = []
        for option in value:
                searches.append(option['value'])
        for search in searches:
                search_data['sel_subj'] = search
                r = s.post(url, data=search_data, headers=headerss)
                innerSoup = bs(r.text,'html.parser')
                value = innerSoup.find('tbody')
                class_title = innerSoup.find_all('td', attrs={'class':'nttitle'}, recursive = True)
                class_info = innerSoup.find_all('td', attrs={'class':'ntdefault'}, recursive = True)
                if search_data['sel_subj'] == "ADMN":
                        print(class_title)
                '''
                As of right now, this will get relevant information in each of 
                the searches possible. The next step is to only collect data that
                has a link under the type of class, then gather data from that 
                particular link.
                '''


