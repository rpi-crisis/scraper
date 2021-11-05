import requests as rq, json, re
from bs4 import BeautifulSoup as bs


# Scrapes the degrees off of the RPI Catalog.
# AUTHOR: Max Hutz <hutzm@rpi.edu>


################################################################################


def extract_data(html):
  regex = re.compile(r"<div id=\"pp\d+\" class=\"r\d+\">(.+?)</div>", flags=re.DOTALL)
  matches = regex.findall(html)

  return ''.join(matches)


def parse_table(table):
  return {}


def parse_text(soup):
  result = {}

  name, rest = soup.find_all("center", recursive=False)
  table = soup.table.find_all("tr", recursive=False)

  while True:
    result[name.h4.span.text] = parse_table(table)[2:]

    centers = rest.find_all("center", recursive=False)
    if len(centers) != 2:
      return result
    else:
      name, rest = centers


def parse_site():
  # Get HTML from website.
  website = "https://sis.rpi.edu/reg/zs202109.htm"
  html = rq.get(website).text

  text = extract_data(html)
  soup = bs(text, "html.parser")

  data = parse_text(soup)

  return data


################################################################################

if __name__ == '__main__':
  data = parse_site()
  # Output to file.
  out = open("out.json", "w")
  json.dump(data, out)