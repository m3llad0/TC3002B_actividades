from delta import Compiler, Phase


source = '#x0FF1ce'

c = Compiler('program')
c.realize(source)

print(c.wat_code)
print()
print(c.result)