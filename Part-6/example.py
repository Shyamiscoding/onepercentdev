# x = 10
# y = 20
# print(f"Sum: {x + y}")


# import tokenize
# import io
# tokens = tokenize.generate_tokens(io.StringIO("x = 10").readline)
# for tok in tokens:
#     print(tok)


# import ast
# tree = ast.parse("x = 10")
# print(ast.dump(tree, indent=2))

import dis
dis.dis("x = 10")

