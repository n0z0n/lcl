import ast
import astunparse
import argparse


class RewriteFor(ast.NodeTransformer):

    def visit_For(self, node):
        # mangling _{original_name}_{original_lineno}
        iterID = '_{}_{}'.format(node.target.id, node.lineno)
        iterAssignNode = ast.Assign(
            targets=[ast.Name(id=iterID, ctx=ast.Store())],
            value=[
                ast.Call(
                    func=ast.Name(id='iter', ctx=ast.Load()),
                    args=[node.iter],
                    keywords=[])
            ])
        tryNode = ast.Try(
            body=[
                ast.Assign(
                    targets=[ast.Name(id=node.target.id, ctx=ast.Store())],
                    value=[
                        ast.Call(
                            func=ast.Name(id='next', ctx=ast.Load()),
                            args=[ast.Name(id=iterID, ctx=ast.Load())],
                            keywords=[])
                    ])
            ] + [self.visit(body) for body in node.body],
            handlers=[
                ast.ExceptHandler(
                    type=ast.Name(id='StopIteration', ctx=ast.Load()),
                    name=None,
                    body=[node.orelse, ast.Break()])
            ],
            orelse=[],
            finalbody=[])

        whileNode = ast.While(
            test=ast.NameConstant(value=True), orelse=[], body=tryNode)

        return [
            iterAssignNode,
            whileNode,
        ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewirte "for" to "while".')
    parser.add_argument('-i', '--input', required=True, help='source file')
    args = parser.parse_args()
    with open(args.input) as f:
        source = f.readlines()
        source = "".join(source)
    tree = ast.parse(source)
    tree = RewriteFor().visit(tree)
    print(astunparse.unparse(tree))
    exec(astunparse.unparse(tree))
