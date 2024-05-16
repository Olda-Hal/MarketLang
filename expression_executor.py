import ast
import operator

# Definujeme podporované operace
allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}
# this function is used to evaluate the expression
def eval_expr(expr, variables):

    def eval_node(node):
        if isinstance(node, ast.Num): 
            return node.n
        elif isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return allowed_operators[type(node.op)](eval_node(node.operand))
        elif isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            else:
                raise ValueError(f"Variable '{node.id}' is not defined")
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    node = ast.parse(expr, mode='eval').body
    return eval_node(node)

