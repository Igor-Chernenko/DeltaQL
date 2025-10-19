from lark import Lark

with open('grammar.lark', 'r') as f:
    grammar = f.read()

parser = Lark(grammar, start='program', parser='lalr')

code = "var y = 5 + 3"
tree = parser.parse(code)
print(tree.pretty())

