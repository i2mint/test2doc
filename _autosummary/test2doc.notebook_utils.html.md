# test2doc.notebook_utils

Utils for jupyter (ipython) notebooks.

### Functions

| `cells_with_largest_output`(notebook[, n, ...])                                                |                                                                         |
|------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| `clear_outputs_of_cell_ids`(notebook, cell_ids)                                                |                                                                         |
| `clear_outputs_of_largest_output_cells`(notebook)                                              |                                                                         |
| `ensure_notebook_dict`(notebook)                                                               |                                                                         |
| [`get_output_size`](#test2doc.notebook_utils.get_output_size)(cell)                         | Return total size of cell outputs in characters.                        |
| [`sort_notebook_cells`](#test2doc.notebook_utils.sort_notebook_cells)(notebook, \*[, key, ...]) | Sort notebook cells by rank computed by key function (applied to cells) |

### test2doc.notebook_utils.get_output_size(cell)

Return total size of cell outputs in characters.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

### test2doc.notebook_utils.sort_notebook_cells(notebook, \*, key=<function <lambda>>, reverse=False, cell_egress=<function <lambda>>)

Sort notebook cells by rank computed by key function (applied to cells)

* **Parameters:**
  * **notebook** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Path to notebook file or notebook dictionary
  * **key** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)], [`float`](https://docs.python.org/3/builtins/functions.html#float)]) – Function to compute rank from cell dict (default: returns 0)
  * **reverse** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, return largest ranks instead of smallest (default: False)
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`int`](https://docs.python.org/3/builtins/functions.html#int), [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)]]
* **Returns:**
  List of (rank, cell_index, cell_dict) tuples sorted by rank
