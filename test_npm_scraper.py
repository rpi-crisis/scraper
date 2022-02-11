from bs4 import BeautifulSoup as bs
import requests as rq
import re, json, sys, os, json

HEADER = lambda x: '\033[95m' + x + '\033[0m'
OKBLUE = lambda x: '\033[94m' + x + '\033[0m'
OKCYAN = lambda x: '\033[96m' + x + '\033[0m'
OKGREEN = lambda x: '\033[92m' + x + '\033[0m'
WARNING = lambda x: '\033[93m' + x + '\033[0m'
FAIL = lambda x: '\033[91m' + x + '\033[0m'
BOLD = lambda x: '\033[1m' + x + '\033[0m'
UNDERLINE = lambda x: '\033[4m' + x + '\033[0m'


def get_usage():
	print("USAGE: `test_npm_scrapper.py <search_term>`")


def parse_section(section):
	result = {
		"name": "",
		"auth": "",
		"vers": "",
		"desc": "",
	}

	name = section.find("h3", { "class": "db7ee1ac" })
	if name is not None: result["name"] = name.text

	auth = section.find("a", { "class": "e98ba1cc" })
	if auth is not None: result["auth"] = auth.text

	desc = section.find("p", { "class": "_8fbbd57d" })
	if desc is not None: result["desc"] = desc.text

	vers = section.find("span", { "class": "_657f443d" })
	if vers is not None:
		result["vers"] = vers.text.split()[1]

	return result


def elps(string, size):
	string = " ".join(string.splitlines())

	return string.ljust(size) \
			if len(string) <= size \
		else (string[:size - 4] + "...").ljust(size)


def print_data(data):
	len_name = 0
	len_auth = 0
	len_vers = 0

	for package in data:
		len_name = max(len_name, len(package["name"]))
		len_auth = max(len_auth, len(package["auth"]))
		len_vers = max(len_vers, len(package["vers"]))

	len_desc = os.get_terminal_size().columns - len_name - len_auth - len_vers - 3

	for package in data:
		print(BOLD(HEADER(elps(package["name"], len_name))),
					FAIL(elps(package["vers"], len_vers)),
					WARNING(elps(package["auth"], len_auth)),
					OKBLUE(elps(package["desc"], len_desc)))


def print_json(data):
	print(json.dumps(data))


def parse_page(page, search):
	page = f"https://www.npmjs.com/search?q={search}&page={page}&perPage=20"

	data = []

	html = rq.get(page).content.decode('utf-8')
	soup = bs(html, 'html.parser')

	container = soup.find("div", { "class": "d0963384" })
	sections = container.find_all("section")

	for section in sections:
		data.append(parse_section(section))

	return data


def parse_args(args):
	as_json = True
	pages = 1
	search_term = ""

	if len(args) < 2:
		print("ERROR: No search term specified.")
		exit(0)

	search_term = args[1]

	for arg in args[2:]:
		if arg == "--json":
			as_json = True
			continue

		regex = re.compile(r"\-pages=(.+)")
		match = regex.match(arg)

		if match:
			pages = match.group(0)

	return [ as_json, pages, search_term ]


def main():
	[as_json, pages, search_term] = parse_args(sys.argv)

	data = []

	for i in range(pages):
		data.extend(parse_page(i, search_term))

	if as_json:
		print_json(data)
	else:
		print_data(data)

if __name__ == '__main__': main()