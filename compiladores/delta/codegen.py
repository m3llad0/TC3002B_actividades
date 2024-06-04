#codegen.py

from arpeggio import PTNodeVisitor


class CodeGenerationVisitor(PTNodeVisitor):

    WAT_TEMPLATE = ''';; Code generated by the Delta compiler
(module
  (func
    (export "_start")
    (result i32)
{}  )
)
'''

    def __init__(self, symbol_table, **kwargs):
        super().__init__(**kwargs)
        self.__symbol_table = symbol_table

    def visit_program(self, node, children):

        def declare_variables():
            return ''.join([f'    (local ${var_name} i32)\n'
                            for var_name in self.__symbol_table])

        return CodeGenerationVisitor.WAT_TEMPLATE.format(
            declare_variables()
            + ''.join(children))

    def visit_statement(self, node, children):
        return children[0]

    def visit_declaration(self, node, children):
        return ''

    def visit_assignment(self, node, children):
        return children[1] + children[0]

    def visit_lhs_variable(self, node, children):
        name = node.value
        return f'    local.set ${name}\n'

    def visit_if(self, node, children):
        result = (children[0]
                  + '    if\n'
                  + children[1])
        for i in range (2, len(children),1):
            if i % 2 == 0:
                result += ('    else\n'
                           +children[i])  # expression or 'else'
            else:
                result += ('    if\n'
                           +children[i])
            

        result += '    end\n' * (len(children) // 2)
        return result

    def visit_block(self, node, children):
        return ''.join(children)

    def visit_while(self, node, children):
        return (
              '    block\n'
            + '    loop\n'
            + children[0]
            + '    i32.eqz\n'
            + '    br_if 1\n'
            + children[1]
            + '    br 0\n'
            + '    end\n'
            + '    end\n')
    
    def visit_do(self, node, children):
              
        result = ('    loop\n'
                + children[0]
                + children[1]
                + '    br_if 0\n'
                + '    end\n')
        return result

    def visit_expression(self, node, children):
        if len(children) == 1:
            return children[0]
        result = [children[0]]
        for exp in children[1:]:
            result.append('    if (result i32)\n')
            result.append(exp)
        result.append('    i32.eqz\n' * 2)
        result.append((  '    else\n'
                       + '    i32.const 0\n'
                       + '    end\n') * (len(children) - 1))
        return ''.join(result)
    
    def visit_or_expr(self, node, children):
        if len(children) == 1:
            return children[0]

        result = [children[0]]
        for expr in children[1:]:
            result.append('    if(result i32)\n')
            result.append('    i32.const 1\n')
            result.append('    else\n')
            result.append(expr)
        result.append('    i32.eqz\n' * 2)
        result.append('    end\n' * (len(children) - 1))
        return ''.join(result)
    
    def visit_comparison(self, node, children):
        result = [children[0]]
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            if children[i] == '==':
                result.append('    i32.eq\n')
            elif children[i] == '!=':
                result.append('    i32.ne\n')
            elif children[i] == '>=':
                result.append('    i32.ge_s\n')
            elif children[i] == '>':
                result.append('    i32.gt_s\n')
            elif children[i] == '<=':
                result.append('    i32.le_s\n')
            elif children[i] == '<':
                result.append('    i32.lt_s\n')
        return ''.join(result)

    def visit_additive(self, node, children):
        result = [children[0]]
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            match children[i]:
                case '+':
                    result.append('    i32.add\n')
                case '-':
                    result.append('    i32.sub\n')
        return ''.join(result)

    def visit_multiplicative(self, node, children):
        result = [children[0]]
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            match children[i]:
                case '*':
                    result.append('    i32.mul\n')
                case '/':
                    result.append('    i32.div_s\n')
                case '%':
                    result.append('    i32.rem_s\n')
        return ''.join(result)

    def visit_decimal(self, node, children):
        return f'    i32.const { node.value }\n'

    def visit_integer_literal(self, node, children):
        value = None
        if node.value.startswith('#b'):
            value = int(node.value[2:], 2)
        elif node.value.startswith('#o'):
            value = int(node.value[2:], 8)
        elif node.value.startswith('#x'):
            value = int(node.value[2:], 16)
        return f'    i32.const {value}\n'

    def visit_boolean(self, node, children):
        if children[0] == 'true':
            return '    i32.const 1\n'
        else:
            return '    i32.const 0\n'

    def visit_unary(self, node, children):
        result = children[-1]
        for op in children[-2::-1]:
            match op:
                case '+':
                    ... # Do nothing
                case '-':
                    result = (
                          '    i32.const 0\n'
                        + result
                        + '    i32.sub\n'
                    )
                case '!':
                    result += '    i32.eqz\n'
        return result

    def visit_parenthesis(self, node, children):
        return children[0]

    def visit_rhs_variable(self, node, children):
        name = node.value
        return f'    local.get ${name}\n'
