from lark import Lark

grammar_file = open("req_grammar.lark", "r")
grammar = grammar_file.read()

req_file = open("parsing2.txt", "r")
lines = req_file.readlines()

out_file = open("parsing3.txt", "w")

parser = Lark(grammar)

total = 0
good = 0

for line in lines:
	try:
		total += 1
		text = parser.parse(line).pretty() + "\n\n\n\n\n"
		good += 1
		print(text)
	except:
		out_file.write(line)
		pass

print(f"Grammar completed: {good} / {total}, {good / total * 100}%")
out_file.close()
req_file.close()
grammar_file.close()