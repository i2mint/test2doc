# test2doc.base

Base functionality for test2doc

### Functions

| [`are_all_valid_python_code`](#test2doc.base.are_all_valid_python_code)(blocks)                 | True if, and only if, all blocks are valid python code                                           |
|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| [`ast_block_line_coordinates`](#test2doc.base.ast_block_line_coordinates)(src_string)            | Walks AST of src_string, yielding (lineno, end_lineno) coordinates of its nodes, when a node has |
| `blocks_to_docs`(blocks)                                                                           |                                                                                                  |
| [`code_to_docs`](#test2doc.base.code_to_docs)(code)                                | code (multi kinds) -> src_string -> blocks -> docs                                               |
| `code_to_src_string`(code)                                                                         |                                                                                                  |
| [`is_proper_partition`](#test2doc.base.is_proper_partition)(blocks, src_string)           | True if, and only if, the blocks can be assembled to make src_string                             |
| [`is_valid_blocks_of_src_string`](#test2doc.base.is_valid_blocks_of_src_string)(blocks, src_string) | True, and only if, the blocks have valid python and                                              |
| [`is_valid_python_code`](#test2doc.base.is_valid_python_code)(src_string)                  | True if, and only if, `src_string` is valid python.                                              |
| [`line_blocks`](#test2doc.base.line_blocks)(lines, line_indices)                  | Generate blocks from lines and line_indices.                                                     |
| `real_line_indices`(line_indices)                                                                  |                                                                                                  |
| [`src_string_to_blocks`](#test2doc.base.src_string_to_blocks)(src_string)                  | Blocks of executable strings taken from `src_string`                                             |

### test2doc.base.are_all_valid_python_code(blocks)

True if, and only if, all blocks are valid python code

### test2doc.base.ast_block_line_coordinates(src_string)

Walks AST of src_string, yielding (lineno, end_lineno) coordinates of its nodes,
when a node has

### test2doc.base.code_to_docs(code)

code (multi kinds) -> src_string -> blocks -> docs

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### test2doc.base.is_proper_partition(blocks, src_string)

True if, and only if, the blocks can be assembled to make src_string

### test2doc.base.is_valid_blocks_of_src_string(blocks, src_string)

True, and only if, the blocks have valid python and

### test2doc.base.is_valid_python_code(src_string)

True if, and only if, `src_string` is valid python.
Valid python is defined as ‘ast.parse(src_string)\` doesn’t raise a `SyntaxError`’

### test2doc.base.line_blocks(lines, line_indices)

Generate blocks from lines and line_indices.
`line_indices` are (i, j) pairs; what will be generated are the
`'\n'`.join(lines[i:j])\`\` strings

* **Return type:**
  [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### test2doc.base.src_string_to_blocks(src_string)

Blocks of executable strings taken from `src_string`
