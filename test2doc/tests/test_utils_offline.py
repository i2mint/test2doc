"""Tests for base conversion helpers, doctest_utils and notebook_utils."""

import json

import pytest

from test2doc import doctest_utils as du
from test2doc import notebook_utils as nu
from test2doc.base import (
    are_all_valid_python_code,
    blocks_to_docs,
    code_to_docs,
    is_proper_partition,
    is_valid_blocks_of_src_string,
    is_valid_python_code,
    src_string_to_blocks,
)


def test_validity_helpers():
    assert is_valid_python_code("x = 1") and not is_valid_python_code("x =")
    assert are_all_valid_python_code(["a = 1", "b = 2"])
    assert not are_all_valid_python_code(["a = 1", "b ="])
    assert is_proper_partition(["a = 1", "b = 2"], "a = 1\nb = 2")
    assert not is_proper_partition(["a = 1"], "a = 1\nb = 2")
    assert is_valid_blocks_of_src_string(["a = 1", "b = 2"], "a = 1\nb = 2")


def test_blocks_to_docs_alternates_text_and_code():
    docs = blocks_to_docs(["# a comment", "x = 1", "y = 2", "# more"])
    assert docs.startswith(" a comment\n")
    assert "```python\nx = 1\ny = 2\n```" in docs
    assert docs.rstrip().endswith("more")


def test_code_to_docs_from_string_and_function():
    src = "# intro\nx = 1\n# next\nprint(x)"
    docs = code_to_docs(src)
    assert "intro" in docs and "```python\nx = 1\n```" in docs
    assert src_string_to_blocks(src)  # non-empty

    def demo():
        # say hi
        greeting = "hi"
        return greeting

    assert "greeting" in code_to_docs(demo)


def test_doctest_utils():
    assert du.remove_assertion("assert x == 1\nplain") == "x\nplain"
    assert (
        du.assertions_to_doctest(">>> assert f(1) == 2\nother")
        == ">>> f(1)\n2\nother\n"
    )
    out = du.txt_to_doctest_txt("a = 1\n    b = 2\n")
    assert out.splitlines()[0] == ">>> a = 1"
    assert out.splitlines()[1].startswith("...\t")
    assert out.splitlines()[-1] == ">>> "


NB = {
    "cells": [
        {"id": "a", "outputs": [{"text": ["12345"]}]},
        {"id": "b", "outputs": [{"data": {"text/plain": "123", "image/png": ["ab", "c"]}}]},
        {"id": "c"},
    ]
}


def test_notebook_dict_and_sizes(tmp_path):
    assert nu.ensure_notebook_dict(NB) is NB
    p = tmp_path / "n.ipynb"
    p.write_text(json.dumps(NB))
    assert nu.ensure_notebook_dict(str(p)) == NB
    with pytest.raises(FileNotFoundError):
        nu.ensure_notebook_dict(str(tmp_path / "missing.ipynb"))
    assert [nu.get_output_size(c) for c in NB["cells"]] == [5, 6, 0]


def test_sort_and_largest():
    ids = [c["id"] for c in nu.sort_notebook_cells(NB, key=nu.get_output_size, reverse=True)]
    assert ids == ["b", "a", "c"]
    assert nu.cells_with_largest_output(NB, n=2) == [
        {"id": "b", "output_size": 6},
        {"id": "a", "output_size": 5},
    ]
    with pytest.raises(ValueError, match="Invalid notebook"):
        list(nu.sort_notebook_cells({"nope": 1}))


def test_largest_default_n_on_small_notebook():
    assert len(nu.cells_with_largest_output(NB)) == 3


def test_clear_outputs():
    import copy

    nb = copy.deepcopy(NB)
    out = nu.clear_outputs_of_cell_ids(nb, {"a"})
    assert out["cells"][0]["outputs"] == [] and out["cells"][1]["outputs"]
    nb2 = copy.deepcopy(NB)
    nu.clear_outputs_of_largest_output_cells(nb2, n=1)
    assert nb2["cells"][1]["outputs"] == []
