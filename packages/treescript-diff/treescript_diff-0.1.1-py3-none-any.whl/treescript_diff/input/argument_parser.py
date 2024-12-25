"""Defines and Validates Argument Syntax.

Encapsulates Argument Parser.

Returns Argument Data, the args provided by the User.
"""
from argparse import ArgumentParser
from sys import exit
from typing import Optional

from .argument_data import ArgumentData
from .string_validation import validate_name


def parse_arguments(args: Optional[list[str]] = None) -> ArgumentData:
    """
    Parse command line arguments.

    Parameters:
    - args: A list of argument strings.

    Returns:
    ArgumentData : Container for Valid Argument Data.
    """
    if args is None or len(args) == 0:
        exit("No Arguments given. ")
    # Initialize the Parser and Parse Immediately
    try:
        parsed_args = _define_arguments().parse_args(args)
        return _validate_arguments(parsed_args)
    except SystemExit:
        exit("Unable to Parse Arguments.")


def _validate_arguments(
    parsed_arguments
) -> ArgumentData:
    """
    Checks the values received from the ArgParser.
        Uses Validate Name method from StringValidation.

    Parameters:
    - parsed_arguments : The object returned by the ArgmentParser.

    Returns:
    ArgumentData - A DataClass of syntactically correct arguments.
    """
    original = parsed_arguments.original
    updated = parsed_arguments.updated
    if not validate_name(original):
        exit("The original argument was invalid.")
    if not validate_name(updated):
        exit("The updated argument was invalid.")
    # Determine diff output
    if parsed_arguments.added or parsed_arguments.removed:
        diff_output = parsed_arguments.added
    else:
        diff_output = None
    #
    return ArgumentData(
        original=original,
        updated=updated,
        diff_output=diff_output,
    )


def _define_arguments() -> ArgumentParser:
    """
    Initializes and Defines Argument Parser.
       - Sets Required/Optional Arguments and Flags.

    Returns:
    argparse.ArgumentParser - An instance with all supported Arguments.
    """
    parser = ArgumentParser(
        description="Tree Script Builder"
    )
    # Required arguments
    parser.add_argument(
        'original',
        type=str,
        help='The original TreeScript.',
    )
    parser.add_argument(
        'updated',
        type=str,
        help='The updated TreeScript.',
    )
    parser.add_argument(
        "--added", '-a',
        action='store_true',
        default=False,
        help='Whether to show added files.',
    )
    parser.add_argument(
        "--removed", '-r',
        action='store_true',
        default=False,
        help='Whether to show deleted files.',
    )
    return parser
