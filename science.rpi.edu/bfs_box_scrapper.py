import requests as rq, json, re
from bs4 import BeautifulSoup as bs

# Breadth-first search for all them boxes and pdfs.

################################################################################


def get_html(site: str):
  return rq.get(site).text


def get_boxes(seed: str):
  visited_sites = []
  boxes_found = []
  sites_to_search = [seed]
  link_regex = r".<a.+?href=\"(?P<url>.+?)\""
  box_regex = r"box"

  while len(sites_to_search) > 0:
    next_site = sites_to_search[0]

    if len(sites_to_search) == 1:
      sites_to_search.pop()
    else:
      sites_to_search[0] = sites_to_search.pop()

    if next_site in visited_sites: continue

    print (f"Search link: {next_site}")
    visited_sites.append(next_site)

    html = get_html(next_site)
    matches = re.findall(link_regex, html)

    if not matches: continue
    
    for url in matches:
      box_link = re.match(box_regex, url)

      if box_link:
        if url in boxes_found: continue
        boxes_found.append(url)
        print(f"Box found: {url}")
      else:
        if url in visited_sites: continue
        sites_to_search.append(url)
        print(f"Link found: {url}")

    return boxes_found


################################################################################

if __name__ == '__main__':
  data = get_boxes("https://science.rpi.edu/")
  # Output to file.
  out = open("out.json", "w")
  json.dump(data, out)