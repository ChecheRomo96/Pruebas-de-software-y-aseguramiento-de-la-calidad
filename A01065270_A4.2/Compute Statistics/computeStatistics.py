"""
compute_statistics.py

This script reads a file containing numbers and computes various statistical
measures, including mean, median, mode, variance, and standard deviation.

It outputs the results to both the console and a results file.

Usage:
    python compute_statistics.py <file_with_data.txt>

Output:
    A file named 'results/StatisticsResults.<input_filename>' containing the
    computed statistics.

Functions:
    - read_numbers_from_file(filename): Reads numbers from a file.
    - compute_mean(numbers): Computes the mean (average).
    - compute_median(numbers): Computes the median.
    - compute_mode(numbers): Computes the mode(s).
    - compute_variance(numbers, mean): Computes the variance.
    - compute_standard_deviation(variance): Computes the standard deviation.
    - main(): Pipeline for orchestrating the operation.
"""

import sys
import os
import time
import math
from collections import Counter


def read_numbers_from_file(filename):
    """
    Reads numbers from a given file.

    Args:
        filename (str): Path to the input file.

    Returns:
        list of float: A list of numbers extracted from the file.
    """
    numbers = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    numbers.append(float(line.strip()))
                except ValueError:
                    print(f"Warning: Ignoring invalid data - {line.strip()}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    return numbers


def compute_mean(numbers):
    """
    Computes the mean (average) of a list of numbers.

    Args:
        numbers (list of float): The list of numbers.

    Returns:
        float: The mean value, or NaN if the list is empty.
    """
    return sum(numbers) / len(numbers) if numbers else float('nan')


def compute_median(numbers):
    """
    Computes the median of a list of numbers.

    Args:
        numbers (list of float): The list of numbers.

    Returns:
        float: The median value, or NaN if the list is empty.
    """
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n == 0:
        return float('nan')
    mid = n // 2
    if n % 2 != 0:
        return sorted_numbers[mid]
    return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2


def compute_mode(numbers):
    """
    Computes the mode(s) of a list of numbers.

    Args:
        numbers (list of float): The list of numbers.

    Returns:
        float, list, or str: The mode value, list of modes (if multiple),
                             or "N/A" if there is no mode.
    """
    if not numbers:
        return "N/A"
    frequency = Counter(numbers)
    max_count = max(frequency.values(), default=0)
    modes = [num for num, count in frequency.items() if count == max_count]
    if len(modes) == len(set(numbers)):
        return "N/A"
    return modes if len(modes) > 1 else modes[0]


def compute_variance(numbers, mean):
    """
    Computes the variance of a list of numbers.

    Args:
        numbers (list of float): The list of numbers.
        mean (float): The mean of the numbers.

    Returns:
        float: The variance value, or NaN if the list is empty.
    """
    if not numbers:
        return float('nan')

    return sum((x - mean) ** 2 for x in numbers) / len(numbers)


def compute_standard_deviation(variance):
    """
    Computes the standard deviation of a dataset.

    Args:
        variance (float): The variance of the dataset.

    Returns:
        float: The standard deviation, or NaN if variance is NaN.
    """
    return math.sqrt(variance) if not math.isnan(variance) else float('nan')


def main():
    """
    Main function that reads numbers from a file,
    computes statistics, and writes results to an
    output file.

    Usage:
        python compute_statistics.py <file_with_data.txt>

    Outputs:
        A file 'results/StatisticsResults.<input_filename>'
        containing computed statistics.
    """
    if len(sys.argv) != 2:
        print("Usage: python compute_statistics.py <file_with_data.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    start_time = time.time()
    numbers = read_numbers_from_file(filename)

    if not numbers:
        print(f"Error: No valid numbers found in {filename}. Skipping.")
        sys.exit(1)

    mean_value = compute_mean(numbers)
    variance_value = compute_variance(numbers, mean_value)

    stats = {
        "Mean": f"{mean_value:.4f}",
        "Median": f"{compute_median(numbers):.4f}",
        "Mode": (
            ", ".join(map(str, compute_mode(numbers)))
            if isinstance(compute_mode(numbers), list)
            else str(compute_mode(numbers))
        ),
        "Variance": f"{variance_value:.4f}",
        "StdDev": f"{compute_standard_deviation(variance_value):.4f}",
        "Time": f"{time.time() - start_time:.6f} s"
    }

    output = (
        f"Mean               : {stats['Mean']}\n"
        f"Median             : {stats['Median']}\n"
        f"Mode               : {stats['Mode']}\n"
        f"Variance           : {stats['Variance']}\n"
        f"Standard Deviation : {stats['StdDev']}\n"
        f"Time               : {stats['Time']}\n"
    )

    print(output)

    try:
        # Ensure results directory exists
        os.makedirs("results", exist_ok=True)
        output_filename = (
            f"results/StatisticsResults.{os.path.basename(filename)}"
        )
        with open(output_filename, "w", encoding="utf-8") as result_file:
            result_file.write(output)
        print(f"Results saved to: {output_filename}")
    except OSError as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
