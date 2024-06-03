from delta import Compiler

source = "1 <= 2 == 1 != 0 > 0 < 0 <= 1"


c = Compiler("program")

c.realize(source)
print(c.wat_code)
print(c.result)


