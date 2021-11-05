"""
Searches and scrapes course information for SIS
without requiring login / two-factor authentication.

A JSON file is generated with additional course information.
"""

import requests as rq, json
from bs4 import BeautifulSoup as bs

headerss = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 \
                         Safari/537.36'
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

# currently non-functional
with rq.Session() as s:
        url = 'https://sis.rpi.edu/rss/bwckctlg.p_display_courses'
        r = s.get(url, headers=headerss)
        soup = bs(r.content,'html.parser')
        searches = soup.find('select', attrs={'name':'sel_subj'}).findAll('option')
        allSearches = searches.findAll('option')['value']
        search_data['sel_subj'] = soup.find('select', attrs={'name':'sel_subj'})
        r = s.post(url, data=search_data, headers=headerss)
        print(r.content)