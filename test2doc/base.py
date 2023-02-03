"""Base functionality for test2doc"""

from i2.tests.test_wrapper import test_mk_ingress_from_name_mapper
import inspect
from typing import Iterable, Generator, Union
import ast
from ast import parse as ast_parse
try:
    # Try ast.parse (3.9+)
    from ast import unparse as ast_unparse
except ImportError:
    from astunparse import unparse as ast_unparse

Blocks = Iterable[str]
StringGenerator = Generator[str, None, None]


def ast_block_line_coordinates(src_string: str):
    """
    Walks AST of src_string, yielding (lineno, end_lineno) coordinates of its nodes,
    when a node has
    """
    for block in ast.walk(ast_parse(src_string)):
        if hasattr(block, 'lineno'):
            yield block.lineno, block.end_lineno


def real_line_indices(line_indices):
    for lower_bound, upper_bound in line_indices:
        yield lower_bound - 1, upper_bound


def line_blocks(lines, line_indices) -> Blocks:
    r"""Generate blocks from lines and line_indices.
    ``line_indices`` are (i, j) pairs; what will be generated are the
    ``'\n'``.join(lines[i:j])`` strings
    """
    for lower_bound, upper_bound in line_indices:
        yield '\n'.join(lines[lower_bound:upper_bound])


def _intervals_and_compliments(sorted_intervals, max_bound=None, min_bound=0):
    """
    Yield the disjoint (i, j) intervals taken from ``sorted_intervals``, also
    yielding the gaps between the input intervals.

    >>> list(_intervals_and_compliments([(2, 4), (5, 6), (6, 8)], max_bound=11))
    [(0, 1), (1, 4), (4, 4), (4, 6), (6, 5), (5, 8), (8, 11)]

    :param sorted_intervals: Sorted (i, j) pairs
    :param max_bound: The lowest index to yield (default 0)
    :param min_bound: The highest index to yield (default is ``sorted_intervals[-1][-1]``
    :return: A generator of integer pairs
    """
    max_bound = max_bound or sorted_intervals[-1][-1]
    max_so_far = min_bound
    for lower_bound, upper_bound in sorted_intervals:
        if upper_bound >= max_so_far:
            yield max_so_far, lower_bound - 1
            yield lower_bound - 1, upper_bound
        max_so_far = max(upper_bound, max_so_far)
    yield max_so_far, max_bound


def src_string_to_blocks(src_string: str):
    """Blocks of executable strings taken from ``src_string``"""
    sorted_ast_block_lines = sorted(set(ast_block_line_coordinates(src_string)))
    # filter out those intervals whose lower bound is higher than the upper bound
    block_indices = list(
        filter(lambda x: x[0] < x[1], _intervals_and_compliments(sorted_ast_block_lines))
    )
    return list(line_blocks(src_string.splitlines(), block_indices))


def _blocks_to_docs_lines(blocks: Blocks) -> StringGenerator:
    for block in blocks:
        if block.strip().startswith('#'):
            yield 'text', block.strip()[1:]
        else:
            yield 'code', block


from itertools import groupby
from operator import itemgetter


def _blocks_to_docs(blocks: Blocks) -> StringGenerator:
    key_getter = itemgetter(0)
    val_getter = itemgetter(1)
    grouped = groupby(_blocks_to_docs_lines(blocks), key=key_getter)
    for kind, section_strs in grouped:
        section = '\n'.join(map(val_getter, section_strs))
        if kind == 'text':
            yield f'{section}\n'
        elif kind == 'code':
            yield f'```python\n{section}\n```\n'


def blocks_to_docs(blocks: Blocks) -> str:
    return '\n'.join(_blocks_to_docs(blocks))


Code = Union[Blocks, str, object]


def code_to_src_string(code: Code) -> str:
    if not isinstance(code, str):
        src_string = inspect.getsource(code)
        tree = ast_parse(src_string)
        first_line_of_body = tree.body[0].body[0].lineno
        body_lines, _ = inspect.getsourcelines(code)
        code = ''.join(body_lines[(first_line_of_body - 1):])
    assert isinstance(code, str)
    return inspect.cleandoc(code)


def code_to_docs(code: Code) -> str:
    """code (multi kinds) -> src_string -> blocks -> docs"""
    # if not isinstance(code, Iterable):
    #     blocks = inspect.getsourcelines(code)[1:]
    # else:
    #     if isinstance(code, str):
    #         blocks = src_string_to_blocks(code)
    #     else:
    #         # consider code to be an iterable of code strings, and glue them together
    #         assert isinstance(code, Iterable), \
    #             f'code should be a string at this point: Was {type(code)}'
    #         blocks = code
    src_string = code_to_src_string(code)
    blocks = src_string_to_blocks(src_string)
    return blocks_to_docs(blocks)


# ---------------------------------------------------------------------------------------
# Validity


def is_valid_python_code(src_string: str):
    """True if, and only if, ``src_string`` is valid python.
    Valid python is defined as 'ast.parse(src_string)` doesn't raise a ``SyntaxError``'
    """
    try:
        ast_parse(src_string)
        return True
    except SyntaxError:
        return False


def are_all_valid_python_code(blocks: Blocks):
    """True if, and only if, all blocks are valid python code"""
    return all(map(is_valid_python_code, blocks))


def is_proper_partition(blocks: Blocks, src_string: str):
    """True if, and only if, the blocks can be assembled to make src_string"""
    blocks = list(blocks)  # to make sure it has a size
    # stripping out extremal spaces
    blocks[0] = blocks[0].strip()
    blocks[-1] = blocks[-1].strip()
    src_string = src_string.strip()
    return '\n'.join(blocks) == src_string


def is_valid_blocks_of_src_string(blocks: Blocks, src_string: str):
    """True, and only if, the blocks have valid python and """
    return are_all_valid_python_code(blocks) and is_proper_partition(blocks, src_string)



