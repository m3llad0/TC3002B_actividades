from delta import Compiler, Phase


source = '10 && 20 && 0'

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
# print(c.parse_tree_str)
# print(c.symbol_table)
# print(c.wat_code)
print(c.result)
