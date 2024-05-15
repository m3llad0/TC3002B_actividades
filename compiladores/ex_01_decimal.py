from delta import Compiler, Phase

source = '42'

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
# print(c.parse_tree_str)
print(c.wat_code)
print(c.result)