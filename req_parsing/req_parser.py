import re, json, sys, os, json
from fuzzywuzzy import fuzz

reqs_file = open("reqs.txt", "r")
coid_file = open("coid.json", "r")

out_file = open("parsing1.txt", "w")

coids = json.load(coid_file)

crse_regex = re.compile(r"[A-Z]{4}[\- ]\d{4}")

# Determines if a string is close enough to be considered a match.
# NOTE: 80% or greater is considered a match.
def cmatch(str1, str2):
	return fuzz.partial_ratio(str1, str2) > 80


def cut_class_names(line):
	global coids

	offset = 0
	result = ""

	matches = crse_regex.finditer(line)
	
	for match in matches:
		name = ""

		try: 
			name = coids[match[0]]
		except KeyError:
			print(match[0])
			continue

		next_start = match.end() + 1
		next_end = next_start + len(name)

		if len(line) <= next_end:
			next_end = len(line) - 1

		next_txt = line[next_start : next_end]

		if cmatch(next_txt, name):
			result += line[offset : next_start - 1]
			offset = next_end

	return result + line[offset:]


def parse(line):
	line2 = cut_class_names(line)

	out_file.write(line2)


def main():
	lines = reqs_file.readlines()

	for line in lines:
		parse(line)

if __name__ == '__main__': main()

reqs_file.close()
coid_file.close()

out_file.close()