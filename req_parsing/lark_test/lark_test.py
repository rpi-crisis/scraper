from lark import Lark


text = """
c red yellow
fill { repeat 36 {
    f200 l170
}}
"""

f = open('turtle_grammar.txt', 'r')
turtle_grammar = f.read()
parser = Lark(turtle_grammar)  # Scannerless Earley is the default
 
print(parser.parse(text).pretty())