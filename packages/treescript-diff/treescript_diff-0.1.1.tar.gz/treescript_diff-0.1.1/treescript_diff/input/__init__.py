"""Validate System Arguments into usable InputData
"""
from treescript_diff.input.argument_parser import parse_arguments
from treescript_diff.input.file_validation import validate_input_file
from .input_data import InputData


def validate_arguments(args: list[str]) -> InputData:
    """
    Validate Command Line Arguments into usable InputData
    """
    arg_data = parse_arguments(args)
    if not (original_tree := validate_input_file(arg_data.original)):
        exit("Original File not found")
    if not (updated := validate_input_file(arg_data.updated)):
        exit("Updated File not found")
    return InputData(
        original_tree=original_tree,
        updated_tree=updated,
        diff_output=arg_data.diff_output,
    )
