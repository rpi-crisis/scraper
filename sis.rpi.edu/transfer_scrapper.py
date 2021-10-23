import requests as rq, json, re
from bs4 import BeautifulSoup as bs


# This parser takes transfer data from SIS, and puts it into a usable format.
# AUTHOR: Max Hutz <hutzm@rpi.edu>


################################################################################
url = "https://sis.rpi.edu/rss/yhwwkwags.P_Select_Inst"


# Fix spaces. Simple.
def fix_spaces(messed_up_string):
  return re.sub(r'\s\s+', ' ', messed_up_string)


# Get transfer html.
# NOTE: SBGI stands for Source/Background Institution Code (apparently).
def get_soup(nation="", state="", sbgi=""):
  site = url + f'?stat_code={state}&natn_code={nation}&sbgi_code={sbgi}'
  html = rq.get(site).text
  soup = bs(html, 'html.parser')
  return soup


# Get the different codes from a tag.
def parse_codes(codes, first=False):
  result = {}
  
  options = codes.findAll("option")
  # Sometimes, the first option is just for filling space or is a non-answer.
  if not first: del options[0]

  for option in options:
    result[option.get("value")] = option.text
  
  return result


# Get all the transfer offers from a certain college.
def parse_college(name, nation="", state="", sbgi=""):
  results = {
    "college_sbgi": sbgi,
    "college_name": name,
    "offers": []
  }

  # Get all of the rows.
  soup = get_soup(nation, state, sbgi)
  rows = soup.findAll("tr")[2:]

  for i in range(len(rows)):
    # Offers can have multiple transfer courses count toward one course here, or
    # have multiple a transfer course that can be put towards multiple courses
    # here.
    offer = {
      "from": [],
      "to": []
    }
    
    while True:
      cells = rows[i].findAll("td")
      # If it encounters the end of an offer, break.
      if len(cells) < 3: break
      # If a credit is not evaluated or not transferable yet, why list it?
      if len(cells) > 3 and \
        (cells[3].text == "Not Transferable" or \
         cells[3].text == "Not Evaluated"): break

      # Some rows have courses from the college that can be transfered.
      if len(cells[1].text) != 1:
        offer["from"].append({
          "code": fix_spaces(cells[1].text.strip()),
          "name": fix_spaces(cells[2].text.strip())
        })

      # And others have courses which credits can be used for.
      if len(cells) == 7 and len(cells[3].text) != 1:
        credit_text = cells[5].text.strip()

        offer["to"].append({
          "code": fix_spaces(cells[3].text.strip()),
          "name": fix_spaces(cells[4].text.strip()),
          # Sometimes credit isn't put down in the table. We keep it in here
          # because this was probably an error with the system, and there is
          # a chance this offer exists.
          "credits": int(credit_text[0]) if len(credit_text) > 0 else -1
        })
      
      i += 1

    # Remove non-offers.
    if len(offer["from"]) != 0:
      results["offers"].append(offer)

  return results


# Get all of the transfers from a state.
def parse_state(state, name):
  results = {
    "state_code": state,
    "state_name": name,
    "colleges": []
  }

  soup = get_soup(state=state)
  # Get them SBGIs!
  sbgi_tag = soup.find("select", { "name": "sbgi_code" })
  sbgi_codes = parse_codes(sbgi_tag, first=True)

  # Parse all colleges in-state.
  for code, college_name in sbgi_codes.items():
    college_offers = parse_college(college_name, sbgi=code, state=state)
    # Some whacky college are listed but without any transferable courses, which
    # should be removed since it serves no purpose.
    if len(college_offers["offers"]) > 0:
      results["colleges"].append(college_offers)

  return results


# Get all of the transfers from a nation.
def parse_nation(nation, name):
  results = {
    "nation_code": nation,
    "nation_name": name,
    "colleges": []
  }

  soup = get_soup(nation=nation)
  # Get them SBGIs!
  sbgi_tag = soup.find("select", { "name": "sbgi_code" })
  sbgi_codes = parse_codes(sbgi_tag, first=True)

  # Parse all colleges in nation.
  for code, college_name in sbgi_codes.items():
    college_offers = parse_college(college_name, sbgi=code, nation=nation)
    # Some whacky college are listed but without any transferable courses, which
    # should be removed since it serves no purpose.
    if len(college_offers["offers"]) > 0:
      results["colleges"].append(college_offers)

  return results


def parse_site():
  results = []
  # Get plain version of website.
  soup = get_soup()

  # Get nation/state codes from html.
  stat_tag = soup.find("select", { "name": "stat_code" })
  state_codes = parse_codes(stat_tag)

  natn_tag = soup.find("select", { "name": "natn_code" })
  nation_codes = parse_codes(natn_tag)

  # Parse all of the state codes for USA and Canada, because they are special
  # snowflakes and are listed differently.
  USA = {
    "nation_code": "US",
    "nation_name": "United States of America",
    "states": []
  }

  Canada = {
    "nation_code": "CA",
    "nation_name": "Canada",
    "states": []
  }

  for code, name in state_codes.items():
    if "Canada" in name:
      # State which are in Canada have names like "..., Canada", so just parse
      # out the comma and 'Canada' and it's good.
      Canada["states"].append(parse_state(code, name.split(",")[0]))
    else:
      USA["states"].append(parse_state(code, name))

  results.append(USA)
  results.append(Canada)

  # Parse all of the codes for all other nations.
  for code, name in nation_codes.items():
    results.append(parse_nation(code, name))

  return results


################################################################################

if __name__ == '__main__':
  data = parse_site()
  # Dump it into a json file.
  out = open("out.json", "w")
  json.dump(data, out)