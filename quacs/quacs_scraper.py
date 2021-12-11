import requests as rq
import json
import re

# Gets QuACS data and parses into a format that CRISIS can use.

# NOTE: Some classes will ONLY have title, department, id_num, and desciprtion
# because courses.json and catalog.json don't always have the same classes.


# Helper splice function
def splice(string, index, char):
  return string[:index] + char + string[(index + 1):]


# courses.json #################################################################


# Takes each of the courses in courses.json and sorts them instead by class.
def parse_majors(out, data):
  # Go and parse through each major.
  for major in data:
    parse_courses(out, major["courses"])


# Helper function to sort courses found within a specific major.
def parse_courses(out, courses):
  for course in courses:
    credits, CRNs = parse_sections(course)
    # IDs are represented as four digit numbers, so '12' should be instead be
    # '0012'.
    id = "{:04d}".format(course["crse"])
    # This will make it very simple to sort by class.
    name = course["subj"] + "-" + id
 
    out[name] = {
      "title": course["title"],
      "crns": CRNs,
      "credits": credits,
      "department": course["subj"],
      "id_num": id,
      # This will be filled out by transfer.json.
      "transfer": [],
      # It is assumed false, and hass_pathways.json will correct all that are.
      "ci": "false",
      # This will be further by other sources.
      "required_by": {
        "major": [],
        "minor": [],
        "hass": []
      }
    }


# Helper function to find the CRNs and credits a course.
def parse_sections(course):
  CRNs = []
  # Credits should be the same for each class, so it doesn't matter which class
  # to get the credits from.
  credMax = course["sections"][0]["credMax"]
  credMin = course["sections"][0]["credMax"]

  credits = ""
  # If classes can be taken for different amounts of credits, represent credits
  # as a range.
  if credMax != credMin:
    credits = str(credMin) + '-' + str(credMax)
  else:
    credits = str(credMax)

  # Get CRNs
  for section in course["sections"]:
    CRNs.append(section["crn"])
  
  return credits, CRNs


# catalog.json #################################################################


# Takes takes the descriptions of classes and puts them with the result.
def parse_descriptions(out, data):
  for key, value in data.items():
    # Some classes exist in catalog.json but not courses.json,
    if key in out:
      out[key]['description'] = value['description']
    else:
      # in which case all available data from catalog.json will be used to repr-
      # esent the class.
      out[key] = {
        "department": value['subj'],
        "id_num": value['crse'],
        "title": value['name'],
        "description": value['description'],
        # This will be filled out by transfer.json.
        "transfer": [],
        # It is assumed false, and hass_pathways.json will correct all that are.
        "ci": "false",
        # This will be further by other sources.
        "required_by": {
          "major": [],
          "minor": [],
          "hass": []
        }
      }


# prerequisites.json ###########################################################


# Given a CRN, it finds its respective class
def get_class_from_crn(CRN, data):
  for key, value in data.items():
    if ('crns' in value) and \
       (int(CRN) in value['crns']):
      return key
  return None


# NOTE: This function flattens the requirement tree, only giving you a set of
# all classes present in it.
def get_prereqs(data):
  switch = data["type"]
  if switch == "course":
    return [data["course"]]
  elif (switch == "or") or (switch == "and"):
    result = []
    for x in data["nested"]: result += get_prereqs(x)
    return [*set(result)]
  else: print("Error: cannot parse type: " + switch)


# Adds prerequisite data into the CRISIS data
def parse_prereqs(out, data):
  for key, value in data.items():
    # If a CRN doesn't have any prerequisites, why go through the trouble to get
    # its class?
    if value and ("prerequisites" in value):
      course = get_class_from_crn(key, out)
      # If a CRN doesn't have a defined class, forget about it.
      if course:
        out[course]["prereq"] = get_prereqs(value["prerequisites"])


# transfer.json ################################################################


# Adds transfer courses to the data.
def parse_tranfers(out, data):
  for key, courses in data.items():
    class_name = splice(key, 4, '-')

    # Classes wich were not already documented are ignored.
    if class_name not in out: continue

    for course in courses:
      for item in course["transfer"]:
        transfer = {
          "school": course["school_name"],
          "location": course["location"]
        }

        # Some transfer courses don't have name or id specified.
        if "name" in item: transfer["title"] = item["name"]
        if "id" in item: transfer["id"] = item["id"]

        out[class_name]["transfer"].append(transfer)


# hass_pathways.json ###########################################################


# Parses each required class string in hass_pathways.json
# NOTE: this is not perfect, as certain expressions like "IHSS 19XX" are not
# understood.
def parse_required_courses(out, string, hass):
  regex = r"[A-Z]{4} \d{4}"
  matches = re.findall(regex, string)

  for match in matches:
    # We want 'XXXX-YYYY' not 'XXXX YYYY'
    match = splice(match, 4, '-')

    if match in out:
      out[match]["required_by"]["hass"].append(hass)


# Parses the pathways in hass_pathways.json
# NOTE: this does not take into account sets of classes, where only some
# combination needs to be taken, but not each one specifically.
def parse_pathways(out, data):
  for hass, desc in data.items():
    if "required" not in desc: continue

    for required_class in desc["required"]:
      parse_required_courses(out, required_class, hass)


################################################################################


# Get courses.json
courses = "https://raw.githubusercontent.com/quacs/quacs-data/master/semester_data/202201/courses.json"
courses_json = rq.get(courses).text
courses_data = json.loads(courses_json)

# Get catalog.json
catalog = "https://raw.githubusercontent.com/quacs/quacs-data/master/semester_data/202201/catalog.json"
catalog_json = rq.get(catalog).text
catalog_data = json.loads(catalog_json)

# Get prerequisites.json
prereqs = "https://raw.githubusercontent.com/quacs/quacs-data/master/semester_data/202201/prerequisites.json"
prereqs_json = rq.get(prereqs).text
prereqs_data = json.loads(prereqs_json)

# Get transfer.json
transfer = "https://raw.githubusercontent.com/quacs/quacs-data/master/transfer.json"
transfer_json = rq.get(transfer).text
transfer_data = json.loads(transfer_json)

# Get hass_pathways.json
pathways = "https://raw.githubusercontent.com/quacs/quacs-data/master/hass_pathways.json"
pathways_json = rq.get(pathways).text
pathways_data = json.loads(pathways_json)


data = {}
# Parse data
parse_majors(data, courses_data)
parse_descriptions(data, catalog_data)
parse_prereqs(data, prereqs_data)
parse_tranfers(data, transfer_data)
parse_pathways(data, pathways_data)


with open("out.json", "w") as out:
  json.dump(data, out)