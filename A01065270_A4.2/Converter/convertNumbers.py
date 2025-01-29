"""
convert_numbers.py

This script reads a file containing numbers and converts each number 
to its binary and hexadecimal representations without using built-in 
conversion functions.

Usage:
    python convert_numbers.py <filename>

Output:
    A file named 'conversion_results.txt' with formatted results.
"""

import sys
import time
import math


def to_binary(n):
    """Convert a number to binary representation without built-in functions."""
    if n == 0:
        return "0"
    binary = ""
    while n > 0:
        binary = str(n % 2) + binary
        n //= 2
    return binary


def to_hexadecimal(n):
    """Convert a number to hexadecimal representation without built-in functions."""
    hex_digits = "0123456789ABCDEF"
    if n == 0:
        return "0"
    hexadecimal = ""
    while n > 0:
        hexadecimal = hex_digits[n % 16] + hexadecimal
        n //= 16
    return hexadecimal


def process_file(input_file):
    """
    Process the input file, converting numbers to binary and hexadecimal.

    Args:
        input_file (str): Path to the input file.

    Generates:
        A text file 'conversion_results.txt' with formatted results.
    """
    output_file = "conversion_results.txt"
    start_time = time.time()

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    numbers = [int(line) for line in lines if line.isdigit()]
    max_number = max(numbers, default=1)

    # Calculate max widths only once
    max_width = len(str(max_number))
    max_width_bin = int(math.log2(max_number)) + 1 if max_number > 0 else 1
    max_width_hex = int(math.log(max_number, 16)) + 1 if max_number > 0 else 1

    results = [
        f"{int(line):>{max_width}} -> Binary: {to_binary(int(line)):>{max_width_bin}}, "
        f"Hexadecimal: {to_hexadecimal(int(line)):>{max_width_hex}}"
        if line.isdigit() else f"Invalid data: {line}"
        for line in lines
    ]

    execution_time = time.time() - start_time
    results.append(f"Execution Time: {execution_time:.6f} seconds")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))

    print("\n".join(results))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_numbers.py <filename>")
    else:
        process_file(sys.argv[1])
