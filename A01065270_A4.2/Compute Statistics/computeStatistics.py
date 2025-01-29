import sys
import os
import glob
import time
import math
from collections import Counter

def read_numbers_from_file(filename):
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
    return sum(numbers) / len(numbers) if numbers else float('nan')

def compute_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n == 0:
        return float('nan')
    mid = n // 2
    return sorted_numbers[mid] if n % 2 != 0 else (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2

def compute_mode(numbers):
    if not numbers:
        return "N/A"
    frequency = Counter(numbers)
    max_count = max(frequency.values(), default=0)
    modes = [num for num, count in frequency.items() if count == max_count]
    if len(modes) == len(set(numbers)):
        return "N/A"
    return modes if len(modes) > 1 else modes[0]

def compute_variance(numbers, mean):
    return sum((x - mean) ** 2 for x in numbers) / len(numbers) if numbers else float('nan')

def compute_standard_deviation(variance):
    return math.sqrt(variance) if not math.isnan(variance) else float('nan')

def main():
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

    Output = (
        f"Mean               : {stats["Mean"]}\n"
        f"Median             : {stats["Median"]}\n"
        f"Mode               : {stats["Mode"]}\n"
        f"Variance           : {stats["Variance"]}\n"
        f"Standard Deviation : {stats["StdDev"]}\n"
        f"Time               : {stats["Time"]}\n"
    )

    print(Output)

    try:
        with open(f"results/StatisticsResults.{os.path.basename(filename)}", "w", encoding="utf-8") as result_file:
            result_file.write(Output)
        print(f"results/StatisticsResults.{os.path.basename(filename)}")
    except OSError as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
