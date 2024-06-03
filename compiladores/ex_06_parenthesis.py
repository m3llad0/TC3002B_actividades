from delta import Compiler, Phase


source = '6/2*(1+2)'

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
# print(c.parse_tree_str)
# print(c.wat_code)
print(c.result)
