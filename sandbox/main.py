import ast
import astunparse
import argparse
import rewriteFor
import rewriteFunction

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewirte "for" to "while".')
    parser.add_argument('-i', '--input', required=True, help='source file')
    args = parser.parse_args()
    with open(args.input) as f:
        source = f.readlines()
        source = "".join(source)
    tree = ast.parse(source)
    tree = rewriteFor.RewriteFor().visit(tree)
    tree = rewriteFunction.RewriteFunction().visit(tree)
    print(astunparse.unparse(tree))
    exec(astunparse.unparse(tree))

