#!/usr/bin/env python3
"""
A script to convert epoch timestamps to UTC in a file.
As of right now, this script will not match and convert epoch
timstamps that don't include milliseconds or microseconds. For
example: '1685297729.930423' or '1685297729.930'

When run, the script will output a new file at the location of
the targeted file with '.utc' appended to the original filename.
The orginal file is left unaltered.

The filename argument can use a relative or absolute file path.

Usage:
python3 convert_epoch_to_utc.py ./path/to/file.txt
"""

__author__ = "Evan Wilkerson"
__version__ = "0.0.1-beta"

import argparse
import datetime
import re
import sys
import os


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments object.

    """
    # Create an ArgumentParser object for parsing command-line arguments
    parser = argparse.ArgumentParser(description="Convert epoch timestamps to UTC in a file")

    # Add the 'input_filpath' argument to the parser
    parser.add_argument("input_filepath", help="Path to the file to convert")

    # Parse the command-line argument(s) and store them in the 'args' variable
    args = parser.parse_args()

    # Return the parsed command-line argument(s)
    return args


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def convert_epoch(input_filepath: str, output_filepath: str) -> None:
    """
    Convert epoch timestamps to UTC in the input file and write the modified content to the output file.

    Args:
        input_filepath (str): Path to the input file.
        output_filepath (str): Path to the output file.
    """
    timestamp_regex = r"(\d{10}\.(\d{6}|\d{3}))"
    timestamp_pattern = re.compile(timestamp_regex)
    with open(input_filepath, "r") as input_file, open(output_filepath, "w") as output_file:
        modified_lines = []
        for line in input_file:
            matches = timestamp_pattern.findall(line)
            if matches:
                for match in matches:
                    epoch_timestamp = float(match[0])
                    utc_timestamp = datetime.datetime.utcfromtimestamp(epoch_timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
                    line = line.replace(match[0], utc_timestamp)
            modified_lines.append(line)
        output_file.writelines(modified_lines)


def main():
    """
    Main entry point of the program.
    """
    try:
        args = parse_arguments()

        input_filepath = args.input_filepath
        output_filepath = f"{input_filepath}.utc"

        if file_exists(output_filepath):
            print(f"Output filename already exists: {output_filepath}")
            print("Skipping timestamp conversion... (delete conflicting file and run again, if desired)")
    
        else:
            convert_epoch(input_filepath, output_filepath)
            print(f"Converted file outputed at: '{output_filepath}'")

    except FileNotFoundError:
        print(f"Input file not found: '{input_filepath}'", file=sys.stderr)

    except PermissionError:
        print("Permission denied. Unable to read or write files.", file=sys.stderr)

    except Exception as e:
        print(f"Script error has occurred: {e.__class__.__name__}", file=sys.stderr)

    finally:
        print("Script has completed.")


if __name__ == "__main__":
    main()
