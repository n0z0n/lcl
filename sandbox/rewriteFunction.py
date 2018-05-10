import ast
import inspect
import astunparse


class RewriteFunction(ast.NodeTransformer):
    def __init__(self):
        super().__init__()

    def visit_FunctionDef(self, node):
        print("=============")
        print(ast.dump(node))
        print("=============")
        return ast.Assign(
            targets=[ast.Name(
                id=node.name, ctx=ast.Store())],
            value=ast.Lambda(
                args=ast.arguments(
                    args=node.args.args,
                    vararg=node.args.vararg,
                    kwonlyargs=node.args.kwonlyargs,
                    kw_defaults=node.args.kw_defaults,
                    kwarg=node.args.kwarg,
                    defaults=node.args.defaults),
                body=ast.BoolOp(
                    op=ast.Or(), values=node.body)))
        return node

    def visit_If(self, node):
        print("visit_If")
        return node

    def visit_Name(self, node):
        print("visit_Name")
        return node


if __name__ == '__main__':
    source = '''
def abcde(x=2, y=3):
    print(x,y)
'''

    tree = ast.parse(source)
    # d = ast.dump(tree)
    # print(d)
    #    print(astunparse.unparse(tree))
    tree = RewriteFunction().generic_visit(tree)
    print(astunparse.unparse(tree))
    # exec(astunparse.unparse(tree))
