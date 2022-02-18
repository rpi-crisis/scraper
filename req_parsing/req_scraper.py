from bs4 import BeautifulSoup as bs
import requests as rq
import re, json, sys, os, json

W_CATALOG = "http://catalog.rpi.edu/content.php?"
W_COURSE = "http://catalog.rpi.edu/preview_course.php?"

file = open("reqs.txt", "w", buffering=1)


def get_page(page):
	return W_CATALOG + f"catoid=22&navoid=544&filter[cpage]={page}"


def get_course(course_id):
	return W_COURSE + f"coid={course_id}"


def parse_course_reqs(coid):
	global file

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
			return file.write(reqs.strip().replace(u'\xa0', ' ') + '\n')
		elif part.name == None:
		  reqs += part
		else:
			reqs += part.get_text()


def parse_page(n):
	reqs = []

	page = get_page(n)

	html = rq.get(page).content.decode('utf-8')
	soup = bs(html, 'html.parser')

	table_defaults = soup.find_all("table", { "class": "table_default" }, recursive=True)
	course_table = table_defaults[6]
	
	course_list = course_table.find_all("tr")[1:-2]

	for course in course_list:
		link = course.find("td", { "class": "width" }).a

		print(link['title']);

		coid = link['href'].split("coid=")[1]

		parse_course_reqs(coid)

	return reqs

def main():
	reqs = []


	for i in range(20):
		print(f"========== Page {i + 1} / 20 ==========");

		parse_page(i + 1)


if __name__ == '__main__': main()

file.close()