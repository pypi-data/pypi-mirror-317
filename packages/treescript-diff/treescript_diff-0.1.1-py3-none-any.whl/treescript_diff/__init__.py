"""TreeScript Diff Methods.
"""
from .input.input_data import InputData
from .diff_trees import diff_trees_additions


def ts_diff(data: InputData) -> str:
    """
    The TreeScript Diff main entry point.

    Parameters:
    - data (InputData) : The program input data.

    Returns:
    str - The output of the diff, formatted as requested by InputData.
    """
    new_files = diff_trees_additions(
        data.original_tree,
        data.updated_tree,
    )
    return "\n".join(new_files)
