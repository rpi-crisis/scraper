import requests as rq, json, re
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

# Scrape data on science.rpi.edu regarding a BS degree in Computer Science.
# Author: Max (hutzm@rpi.edu)

MAIN_SITE = "https://science.rpi.edu/computer-science/programs/undergrad/bs-computerscience"

################################################################################

def get_soup(site: str):
  response = rq.get(site)
  if response.status_code == 200:
    return bs(response.text, "html.parser")
  else:
    return False


def faq(question, site):
  question = site.find("h4", text=question)
  top = question.parent.parent.parent
  answer = top.find("div", class_="accordion-content")
  return answer


def parse_main(major, minor, dual, site):
  major_req = faq("Major Requirements - Curriculum Templates", site)
  major_text = major_req.find_all("p")
  concentration = faq("Major Requirements - CS Capstone Concentration Area Courses", site).p.find("a", href=True)
  minor_req = faq("Minor Requirements", site).p
  dual_req = faq("Information for Dual Majors and for Switching to CSCI", site)

  year_rgx = r"\d{4}"

  templates = []
  cells = major_req.ul.find_all("li")
  for cell in cells:
    a = cell.find("a", href=True)
    text = a.text
    match = re.search(year_rgx, text)
    year = match.group(0)
    templates.append({
      "type": "box",
      "name": year,
      "data": a["href"]
    })


  major["requirements"].append({
    "type": "html",
    "name": "DESCRIPTION",
    "data": major_text[0].text + major_text[1].text
  })

  major["requirements"].append({
    "type": "box",
    "name": "CONCENTRATION",
    "data": concentration["href"]
  })

  major["templates"].extend(templates)

  minor["requirements"].append({
    "type": "text",
    "name": "DESCRIPTION",
    "data": minor_req.text
  })

  dual["requirements"].append({
    "type": "html",
    "name": "DESCRIPTION",
    "data": dual_req.get_text()
  })




def get_data():
  major = {
    "type": "major",
    "major": "CSCI",
    "requirements": [],
    "templates": []
  }

  minor = {
    "type": "minor",
    "major": "CSCI",
    "requirements": [],
    "templates": []
  }

  dual = {
    "type": "dual",
    "major": "CSCI",
    "requirements": [],
    "templates": []
  }

  main_site = get_soup(MAIN_SITE)

  parse_main(major, minor, dual, main_site)

  return [ major, minor, dual ]


################################################################################

if __name__ == '__main__':
  data = get_data()
  # Output to file.
  out = open("out.json", "w")
  json.dump(data, out)

