"""Input Data to the Program
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class InputData:
    """The input data to the program.
    """

    original_tree: str
    #
    updated_tree: str
    #
    diff_output: bool | None = None
