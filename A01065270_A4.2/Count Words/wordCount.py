"""
Word Count Script

This script reads a text file, counts the occurrences of
each word, and outputs the word frequency to both the
console and a results file.
"""

import sys
import time
import re
import os


def count_words(file_path):
    """
    Reads a file and counts the occurrences of each word.

    Args:
        file_path (str): The path to the text file.

    Returns:
        dict: A dictionary where keys are words and values
        are their respective counts.
    """
    word_counts = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Extract words, ignoring case
                words = re.findall(r'\b\w+\b', line.lower())
                for word in words:
                    # Simplified dictionary update
                    word_counts[word] = word_counts.get(word, 0) + 1
        return word_counts
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except (OSError, IOError, UnicodeDecodeError) as e:
        print(f"Error processing the file: {e}")
        return None


def write_results(word_counts, elapsed_time):
    """
    Writes the word count results to a file in the 'results' directory.

    Args:
        word_counts (dict): A dictionary of word counts.
        elapsed_time (float): The execution time in seconds.
    """
    try:
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)  # Ensure the directory exists

        output_file_path = os.path.join(
            results_dir,
            f"WordCountResults.{os.path.basename(sys.argv[1])}"
        )

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for word, count in sorted(
                word_counts.items(), key=lambda x: x[1], reverse=True
            ):
                output_file.write(f"{word}\t{count}\n")
                output_file.write(
                    f"\nExecution Time: {elapsed_time:.4f} seconds\n"
                )

        print(f"Results saved in {output_file_path}")

    except (OSError, IOError) as e:  # More specific file-related exceptions
        print(f"Error writing the results file: {e}")


def main():
    """
    Main function that processes the input file,
    counts words, and outputs results.
    """
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <fileWithData.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    start_time = time.time()

    word_counts = count_words(input_file)
    if word_counts is not None:
        elapsed_time = time.time() - start_time
        for word, count in sorted(
            word_counts.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"{word}\t{count}")
        print(f"\nExecution Time: {elapsed_time:.4f} seconds")
        write_results(word_counts, elapsed_time)


if __name__ == "__main__":
    main()
