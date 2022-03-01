from bs4 import BeautifulSoup as bs
import requests as rq
import re, json, sys, os
import unidecode

W_CATALOG = "http://catalog.rpi.edu/content.php?"
W_COURSE = "http://catalog.rpi.edu/preview_course.php?"

YEARS = {
	2021: ("catoid=22&navoid=544", 20),
	2020: ("catoid=21&navoid=521", 20),
	2019: ("catoid=20&navoid=498", 20),
	2018: ("catoid=18&navoid=444", 19),
	2017: ("catoid=16&navoid=390", 19),
	2016: ("catoid=15&navoid=367", 19),
	2015: ("catoid=14&navoid=336", 20),
	2014: ("catoid=13&navoid=313", 19),
	2013: ("catoid=12&navoid=281", 18),
	2012: ("catoid=11&navoid=258", 17),
	2011: ("catoid=10&navoid=233", 17),
	2010: ("catoid=9&navoid=209" , 17),
	2009: ("catoid=8&navoid=187" , 17),
	2008: ("catoid=5&navoid=111" , 18),
	2007: ("catoid=4&navoid=90"  , 18),
}

#req_file = open("reqs.txt", "w")
#coid_file = open("coid.json", "w")

coid_json = {}


def get_page(page, year):
	global YEARS

	return W_CATALOG + YEARS[year][0] + f"&filter[cpage]={page}"


def get_course(course_id):
	return W_COURSE + f"coid={course_id}"


def parse_course_reqs(coid):
	global req_file

	page = get_course(coid)

	html = rq.get(page).content.decode('utf-8')
	soup = bs(html, 'html.parser')

	content = soup.find("td", { "class": "block_content_popup" }, recursive=True)

	parts = [part for part in content.contents]

	reqs = None


	for part in parts:
		if reqs == None:
			if part.name == "strong" and "Prerequisites/Corequisites:" in part.get_text():
				reqs = ""
		elif part.name == "strong":
			return req_file.write(reqs.strip().replace(u'\xa0', ' ') + '\n')
		elif part.name == None:
		  reqs += part
		else:
			reqs += part.get_text()


def parse_page(n, year):
	global coid_json

	page = get_page(n, year)

	html = rq.get(page).content.decode('utf-8')
	soup = bs(html, 'html.parser')

	table_defaults = soup.find_all("table", { "class": "table_default" }, recursive=True)
	course_table = table_defaults[6]
	
	course_list = course_table.find_all("tr")[1:-2]

	for course in course_list:
		link = course.find("td", { "class": "width" }).a
		title = unidecode.unidecode(link['title'].split(" opens a new window")[0])

		stuff = title.split(" - ")
		if len(stuff) != 2: continue

		crse, name = stuff

		crse = crse.upper()

		if crse.strip() not in coid_json:
			coid_json[crse.strip()] = name.strip()
			print(crse)

			coid = link['href'].split("coid=")[1]
			parse_course_reqs(coid)

def main():
	global coid_json, coid_file, YEARS

	for year in YEARS:
		print(f"#*#*#*#*#*#*#*#*# YEAR {year} #*#*#*#*#*#*#*#*#");

		_, pages = YEARS[year]

		for page in range(pages):
			print(f"========== Page {page + 1} / {pages} ==========");

			parse_page(page + 1, year)

	json.dump(coid_json, coid_file)

if __name__ == '__main__': main()

req_file.close()