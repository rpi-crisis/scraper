import requests as rq, json, re
from bs4 import BeautifulSoup as bs


# Scrapes the degrees off of the RPI Catalog.
# AUTHOR: Max Hutz <hutzm@rpi.edu>


################################################################################


def parse_table_rows(out, rows):
  school = ""
  
  for row in rows:
    # There are multiple cells (sometimes) inside each row.
    cells = row.findAll("td", recursive=False)

    # Rows with 5 cells are for individual degree rows.
    if len(cells) == 5:
      # Some rows are blank and only for spacing, so if this fails it's assmued
      # it doesn't have data.
      try:
        degree = cells[0].span.text.strip()
        types = cells[2].span.text.split(',')
        types = [type_.strip() for type_ in types]

        # HEGIS (Higher Education General Information Survey) codes are used in
        # NY to organize degrees by numbers.
        hegis = cells[4].span.text.strip()

        out[school].append({
          "degree": degree,
          "offered": types,
          "hegis": hegis
        })
      except: continue
    else:
      # Rows without 5 cells are for school headings.

      # There are sometimes multiple spans in a header, and only one has a
      # <strong> tag with the school. Those without a strong tab aren't headers
      # and are just there for correct spacing.
      try:
        strong = next(c.strong for c in cells if c.strong)
      except: continue

      # Some schools (like school of engineering) have other tags like <sup> in
      # there text, which shouldn't be taken out (using recursive=False).
      school = strong.span.find(text=True, recursive=False).text.strip()

      # Schools need to be initialized otherwises errors occur.
      out[school] = []


def parse_site():
  # Get HTML from website.
  degrees_website = "http://catalog.rpi.edu/content.php?catoid=22&navoid=525"
  degrees_html = rq.get(degrees_website).text
  soup = bs(degrees_html, 'html.parser')

  # Find the table with all of the data in it.
  table = soup.find_all("table", {
    "border": "0",
    "cellpadding": "0",
    "cellspacing": "0",
    "style": "border-collapse:collapse; height:2027px; width:863px"
  })[0] # There is only one table exactly like this one.

  # The first row is just the table header.
  table_rows = table.tbody.find_all("tr", recursive=False)[1:]

  data = {}
  parse_table_rows(data, table_rows)
  return data


################################################################################

if __name__ == '__main__':
  data = parse_site()
  # Output to file.
  out = open("out.json", "w")
  json.dump(data, out)