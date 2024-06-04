from delta import Compiler

compiler = Compiler("program")

source = """
var n, r, i;
n = 5;
r = 1;
i = 0;
do {
    i = i + 1;
    r = r * i;
} while n - i;
r
"""


compiler.realize(source)

print(compiler.wat_code)
print(compiler.result)  