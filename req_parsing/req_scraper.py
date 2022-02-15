from bs4 import BeautifulSoup as bs
import requests as rq
import re, json, sys, os, json

W_CATALOG = "http://catalog.rpi.edu/content.php?"
W_COURSE = "http://catalog.rpi.edu/preview_course.php?"


def get_page(page):
	return W_CATALOG + f"catoid=22&navoid=544&filter[cpage]={page}"


def get_course(course_id):
	return W_COURSE + f"coid={course_id}"


def parse_course_reqs(coid):
	page = get_course(coid)

	html = rq.get(page).content.decode('utf-8')
	soup = bs(html, 'html.parser')

	content = soup.find("td", { "class": "block_content_popup" }, recursive=True)
	desc_parts = content.find_all()

	for part in desc_parts:
		if part.name == "strong":
			if "Prerequisites/Corequisites:" in part.text:
				return part.next_sibling

	return None


def parse_page(n):
	reqs = []

	page = get_page(n)

	html = rq.get(page).content.decode('utf-8')
	soup = bs(html, 'html.parser')

	table_defaults = soup.find_all("table", { "class": "table_default" }, recursive=True)
	course_table = table_defaults[6]
	
	course_list = course_table.find_all("tr")[1:-2]

	for course in course_list:
		link = course.find("td", { "class": "width" }).a['href']

		coid = link.split("coid=")[1]
		print(coid)

		req = parse_course_reqs(coid)
		if req is not None: reqs.append(req)

	return reqs

def main():
	reqs = []

	reqs.extend(parse_page(1))

	for req in reqs:
		print(req)

if __name__ == '__main__': main()