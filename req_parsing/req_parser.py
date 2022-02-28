import re, json, sys, os, json

file = open("reqs.txt", "r")

# Takes in a string of requirements, and turns it into a string of tokens.
def lexer(line):
	pass

# Takes in a list of tokens, are contructs a tree.
def parser(tokens):
	pass

def main():
	lines = file.readlines()

	for line in lines:
		print(line)

if __name__ == '__main__': main()