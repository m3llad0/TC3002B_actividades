from delta import Compiler
source = '''
var x, y;
x = 5;
if x - 5 {
    y = 1;
} else if x * 0 {
    y = 2;
} else if x - 1 {
    y = 3;
} else {
    y = 4;
}
y
'''

compiler = Compiler("program")

compiler.realize(source)

print(compiler.wat_code)
print(compiler.result)