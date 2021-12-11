import requests as rq, json
from bs4 import BeautifulSoup as bs

def parse_text(out, soup):
    # get the data to pull from
    table = soup.find_all("td", {"class": "block_content", "colspan": "2"})[0]
    table = table.find_all("table")[0]
    codes = table.find_all("tr", recursive = False)[2].find_all("p", recursive = True)
    
    # find the text to remove
    remove_codes = []
    for code in codes:
        if (code.text)[0:18] == "Architecture (SOA)":
            break
        remove_codes.append(code)

    # remove the codes not needed from the list
    for code in remove_codes:
        codes.remove(code)
    
    # split the data accordingly
    for code in codes:
        codes_dict = {}
        code = code.text.strip().split("\n")
        department = code[0].strip()
        for item in code:
            item = item.strip()
            if item != department:
                codes_dict[department]

        data[department] = codes_dict
        print(code)



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
