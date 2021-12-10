import requests as rq, json
from bs4 import BeautifulSoup as bs

if __name__ == "__main__":
    # Get HTML from website.
    codes_website = "http://catalog.rpi.edu/content.php?catoid=22&navoid=543"
    codes_html = rq.get(codes_website).text
    soup = bs(codes_html, 'html.parser')