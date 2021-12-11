import requests as rq, json
from bs4 import BeautifulSoup as bs

def parse_text(out, soup):
    table = soup.find_all("td", {"class": "block_content", "colspan": "2"})[0]
    table = table.find_all("table")[0]

if __name__ == "__main__":
    # Get HTML from website.
    codes_website = "http://catalog.rpi.edu/content.php?catoid=22&navoid=543"
    codes_html = rq.get(codes_website).text
    soup = bs(codes_html, 'html.parser')

    data = {}
    parse_text(data, soup)

    # Ouptut to file
    out = open("subjectCodes.json", "w")
    json.dump(data, out)
