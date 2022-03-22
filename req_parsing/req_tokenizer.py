import re, json, sys, os, json
from fuzzywuzzy import fuzz

reqs_file = open("reqs.txt", "r")
coid_file = open("coid.json", "r")

out_file = open("parsing2.txt", "w")

coids = json.load(coid_file)

crse_regex = re.compile(r"[A-Z]{4}[\- ]?\d{4}")

parsing_spec = [
	('AND', r"\band\b"),
	('NOT', r"\bnot\b"),
	('OR', r"\bor\b"),
	('INS', r"instructor"),
	('GRD', r"graduate"),
	('SEN', r"senior"),
	('JUN', r"junior"),
	('SOF', r"sophomore"),
	('FRS', r"freshman"),
	('REC', r"recommend"),
	('REQ', r"require"),
	('RST', r"restrict"),
	('EXC', r"except"),
	('ARC', r"m\.arch\."),
	('CID', r"\d{4}"),
	('DPT', r"\b[A-Z]{4}\b"),
	('PRE', r"prerequisite"),
	('COR', r"corequisite"),
	('CRS', r"course"),
]

parse_regex = re.compile('|'.join(f"(?P<{pair[0]}>{pair[1]})" for pair in parsing_spec), re.I)

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
		crse = match[0]

		if crse[4] == '-':
			crse = crse[:4] + ' ' + crse[5:]
			line = line[:match.start() + 4] + ' ' + line[match.start() + 5:]
		elif len(crse) == 8:
			crse = crse[:4] + ' ' + crse[4:]
			line = line[:match.start() + 4] + ' ' + line[match.start() + 4:]

		name = ""

		try: name = coids[crse]
		except KeyError: continue

		next_start = match.end() + 1
		next_end = next_start + len(name)

		if len(line) <= next_end:
			next_end = len(line) - 1

		next_txt = line[next_start : next_end]

		if cmatch(next_txt, name):
			result += " " + line[offset : next_start - 1]
			offset = next_end

	return (result + " " + line[offset:]).strip()


def tokenize(line):
	global parse_regex

	tokens = []

	matches = parse_regex.finditer(line)

	for match in matches:
		gdict = match.groupdict()

		for group in gdict:
			txt = gdict[group]

			if txt is not None:
				if group == 'DPT' and not txt.isupper(): continue
				tokens.append((group, txt))

	return tokens

def txt_token(token):
	tok_type, tok_txt = token

	if 	 tok_type == "AND": return  "AND"
	elif tok_type == "OR":  return  "OR"
	elif tok_type == "NOT": return  "NOT"
	elif tok_type == "INS": return  "INSTRUCTOR"
	elif tok_type == "SEN": return  "SENIOR"
	elif tok_type == "JUN": return  "JUNIOR"
	elif tok_type == "SOF": return  "SOPHOMORE"
	elif tok_type == "FRS": return  "FRESHMAN"
	elif tok_type == "REC": return  "RECOMMEND"
	elif tok_type == "REQ": return  "REQUIRE"
	elif tok_type == "RST": return  "RESTRICT"
	elif tok_type == "EXC": return  "EXCEPT"
	elif tok_type == "ARC": return  "M.ARCH."
	elif tok_type == "DPT": return f"[{tok_txt}]"
	elif tok_type == "CID": return f"({tok_txt})"
	elif tok_type == "PRE": return  "PREREQ"
	elif tok_type == "COR": return  "COREQ"
	elif tok_type == "GRD": return  "GRADUATE"
	elif tok_type == "CRS": return  "COURSE"

	return None

def parse(line):
	global out_file

	line2 = cut_class_names(line)

	tokens = tokenize(line2)

	txt = " ".join(txt_token(token) for token in tokens)

	out_file.write(txt + "\n")


def main():
	lines = reqs_file.readlines()

	for line in lines:
		parse(line)

if __name__ == '__main__': main()

reqs_file.close()
coid_file.close()

out_file.close()