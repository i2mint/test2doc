"""Testing base"""

import inspect
from test2doc.base import (
    line_blocks,
    real_line_indices,
    ast_block_line_coordinates,
    src_string_to_blocks,
    is_valid_blocks_of_src_string,
    code_to_src_string,
)


def test_simple():
    def test_func(func, wrap):
        from inspect import signature

        # Just wrapping the func gives you a sort of copy of the func.
        wrapped_func = wrap(func)  # no transformations
        assert wrapped_func(2, 'co') == 'coco' == func(2, 'co')
        assert (
            str(signature(wrapped_func)) == "(a, b: str, c='hi')"
        )  # "(a, b: str, c='hi')"

    src_string = '''from inspect import signature

    # Just wrapping the func gives you a sort of copy of the func.
    wrapped_func = wrap(func)  # no transformations
    assert (
            wrapped_func(2, 'co')
            == 'coco'
            == func(2, 'co')
    )
    assert str(signature(wrapped_func)) == \
           "(a, b: str, c='hi')"  # "(a, b: str, c='hi')"
    '''
    src_string = inspect.cleandoc(src_string)

    assert src_string == code_to_src_string(test_func)

    sorted_ast_block_lines = sorted(set(ast_block_line_coordinates(src_string)))

    # To test that multi-lined expressions work
    t = list(
        line_blocks(src_string.splitlines(), real_line_indices(sorted_ast_block_lines))
    )

    blocks = src_string_to_blocks(src_string)

    # expected_blocks = [
    #     'from inspect import signature',
    #     '',
    #     '# Just wrapping the func gives you a sort of copy of the func.',
    #     'wrapped_func = wrap(func)  # no transformations',
    #     '''assert (
    #             wrapped_func(2, 'co')
    #             == 'coco'
    #             == func(2, 'co')
    #     )''',
    #     '''assert str(signature(wrapped_func)) == \
    #            "(a, b: str, c='hi')"  # "(a, b: str, c='hi')"
    #     ''',
    # ]
    # expected_blocks = list(map(inspect.cleandoc, expected_blocks))
    # # print(blocks)
    # assert blocks == expected_blocks

    # And now validating the blocks, but also testing
    assert is_valid_blocks_of_src_string(blocks, src_string)
