#!/usr/bin/python
from sys import argv

from treescript_diff import ts_diff
from treescript_diff.input import validate_arguments


def main():
    input_data = validate_arguments(argv[1:])
    output_data = ts_diff(input_data)
    print(output_data)


if __name__ == "__main__":
    main()
