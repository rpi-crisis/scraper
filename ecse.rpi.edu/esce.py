import requests as rq, json, re
from bs4 import BeautifulSoup as bs

MAIN_SITE = "https://www.ecse.rpi.edu/academics/undergraduate-programs/program-templates"

################################################################################

def get_soup(site: str):
  response = rq.get(site)
  if response.status_code == 200:
    return bs(response.text, "html.parser")
  else:
    return False

def get_main(major):
  soup = get_soup(MAIN_SITE)

  template_divs = soup.find("article", recursive=True).div.div.ul.find_all("li")

  templates = []

  for template_div in template_divs:
    link = template_div.find("a", href=True)
    href = MAIN_SITE + link["href"]

    templates.append({
      "type": "doc",
      "name": link.text,
      "data": href
    })

  major["templates"].extend(templates)

def get_data():
  major = {
    "type": "major",
    "major": "ESCE",
    "requirements": [],
    "templates": []
  }

  get_main(major)
  return [ major ]

################################################################################

if __name__ == '__main__':
  data = get_data()
  # Output to file.
  out = open("out.json", "w")
  json.dump(data, out)