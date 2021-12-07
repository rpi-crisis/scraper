import requests as rq, json, re
from bs4 import BeautifulSoup as bs

MAIN_SITE = "https://science.rpi.edu/itws/programs/undergrad/bs"

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
  return question, answer

def get_main(major, minor):
  soup = get_soup(MAIN_SITE)
  curric_header = soup.find("h3", text="Curriculum")
  curric_reqs = curric_header.parent.parent.find("div", class_= \
    "view-grouping-content").find("div", class_="view-grouping").find("div", \
    class_="view-grouping-header")
  
  core_header, core_reqs = faq("ITWS Core Requirements (24 - 26 credits)", soup)
  conc_header, conc_reqs = faq("Concentration Requirement (44 credits)", soup)
  degree_header, degree_reqs = faq("Rensselaer Degree Requirements (60 credits)", soup)
  
  major["requirements"].append({
    "type": "html",
    "name": "DESCRIPTION",
    "data": str(curric_header) + str(curric_reqs) +
            str(core_header)   + str(core_reqs)   +
            str(conc_header)   + str(conc_reqs)   +
            str(degree_header) + str(degree_reqs)
  })

  minor_header, minor_reqs = faq("Requirements", soup)

  minor["requirements"].append({
    "type": "html",
    "name": "DESCRIPTION",
    "data": minor_reqs.text
  })

  template_divs = soup.find("h2", text="Documents & Resources").parent.div.div.find_all("div")

  templates = []

  for template_div in template_divs:
    doc_p = template_div.span.p
    link = doc_p.find("a", href=True)
    href = link["href"]

    templates.append({
      "type": "doc",
      "name": link.text,
      "data": href
    })

  major["templates"].extend(templates)


def get_data():
  major = {
    "type": "major",
    "major": "ITWS",
    "requirements": [],
    "templates": []
  }

  minor = {
    "type": "minor",
    "major": "ITWS",
    "requirements": [],
    "templates": []
  }

  get_main(major, minor)
  return [ major, minor ]

################################################################################

if __name__ == '__main__':
  data = get_data()
  # Output to file.
  out = open("out.json", "w")
  json.dump(data, out)