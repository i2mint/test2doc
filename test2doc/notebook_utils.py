"""Utils for jupyter (ipython) notebooks."""

import json
from pathlib import Path
from typing import Union, Callable, List, Tuple


def ensure_notebook_dict(notebook):
    if isinstance(notebook, str):
        nb_path = Path(notebook)
        if not nb_path.exists():
            raise FileNotFoundError(f"Notebook file not found: {notebook}")
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    else:
        nb = notebook

    return nb


def sort_notebook_cells(
    notebook: Union[str, dict],
    *,
    key: Callable[[dict], float] = lambda x: 0,
    reverse: bool = False,
    cell_egress=lambda x: x,
) -> List[Tuple[float, int, dict]]:
    """
    Sort notebook cells by rank computed by key function (applied to cells)

    Args:
        notebook: Path to notebook file or notebook dictionary
        key: Function to compute rank from cell dict (default: returns 0)
        reverse: If True, return largest ranks instead of smallest (default: False)

    Returns:
        List of (rank, cell_index, cell_dict) tuples sorted by rank
    """
    nb = ensure_notebook_dict(notebook)

    if not isinstance(nb, dict) or 'cells' not in nb:
        raise ValueError("Invalid notebook format: must be dict with 'cells' key")

    all_cells = sorted(nb['cells'], key=key, reverse=reverse)
    # Return top n
    return map(cell_egress, all_cells)


def get_output_size(cell: dict) -> int:
    """Return total size of cell outputs in characters."""
    if 'outputs' not in cell:
        return 0
    total_size = 0
    for output in cell['outputs']:
        if 'text' in output:
            total_size += len(''.join(output['text']))
        elif 'data' in output:
            for mime_type, content in output['data'].items():
                if isinstance(content, str):
                    total_size += len(content)
                elif isinstance(content, list):
                    total_size += len(''.join(content))
    return total_size


def _output_size_stats(cell):
    output_size = get_output_size(cell)
    return {'id': cell['id'], 'output_size': output_size}


def cells_with_largest_output(notebook, n=5, cell_egress=_output_size_stats):
    sorted_cells = sort_notebook_cells(
        notebook, key=get_output_size, reverse=True, cell_egress=cell_egress
    )
    return [next(sorted_cells) for _ in range(n)]


def clear_outputs_of_cell_ids(notebook, cell_ids):
    for cell in notebook['cells']:
        if 'id' in cell and cell['id'] in cell_ids:
            cell['outputs'] = []
    return notebook


def clear_outputs_of_largest_output_cells(notebook, n=5, egress=lambda x: x):
    cell_ids = [cell['id'] for cell in cells_with_largest_output(notebook, n)]
    return egress(clear_outputs_of_cell_ids(notebook, cell_ids))
