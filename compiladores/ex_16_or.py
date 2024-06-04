from delta import Compiler

compiler = Compiler("program")

source = '10 || 20 || 30'


compiler.realize(source)

print(compiler.wat_code)

print(compiler.result)