"""
computeSales.py

This script reads product pricing data and sales records from JSON files,
computes total sales for multiple test cases, and writes the results to
a file (`results/Results.txt`).

It supports multiple test case folders (TC1, TC2, ...), each containing:
- A product list JSON (`ProductList.json`)
- A sales record JSON (`Sales.json`)

The script ensures correct data handling, logs invalid items, and
follows PEP8 coding standards.

Usage:
    python computeSales.py
"""
import json
import os
import time

DATA_DIR = "data"
RESULTS_FILE = "results/Results.txt"


def load_json(file_path):
    """Load a JSON file and return its content."""
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return None


def compute_total_sales(price_catalogue, sales_record):
    """
    Compute the total cost of all sales.

    This function aggregates sales quantities from the given sales record,
    calculates the total cost based on the price catalog, and identifies
    any invalid product entries.

    Returns:
        tuple: (total_cost, invalid_entries)
    """
    total_cost = 0.0
    invalid_entries = []

    # Aggregate sales per product
    aggregated_sales = {}

    for entry in sales_record:
        product = entry.get("Product")
        quantity = entry.get("Quantity", 0)

        if product:
            aggregated_sales[product] = (
                aggregated_sales.get(product, 0) + quantity
            )

    # Compute total cost
    for product, quantity in aggregated_sales.items():
        if product in price_catalogue:
            total_cost += price_catalogue[product] * quantity
        else:
            invalid_entries.append(product)

    return total_cost, invalid_entries


def process_test_cases():
    """
    Process multiple test cases (TC1, TC2, TC3, ...) and store results.

    This function scans the `data/` directory for test case folders,
    loads the corresponding `ProductList.json` and `Sales.json` files,
    computes total sales per test case, and writes the results to
     `results/Results.txt`.
    """

    results = []

    for test_case in sorted(os.listdir(DATA_DIR)):
        test_case_path = os.path.join(DATA_DIR, test_case)
        if not os.path.isdir(test_case_path):
            continue  # Skip non-directory files

        # Identify product list and sales files
        product_file = None
        sales_file = None

        for filename in os.listdir(test_case_path):
            if "ProductList" in filename and filename.endswith(".json"):
                product_file = os.path.join(test_case_path, filename)
            elif "Sales" in filename and filename.endswith(".json"):
                sales_file = os.path.join(test_case_path, filename)

        if not product_file or not sales_file:
            print(f"Skipping {test_case} - Missing required files")
            continue

        start_time = time.time()

        # Load JSON data
        price_catalogue_list = load_json(product_file)
        sales_record = load_json(sales_file)

        if price_catalogue_list is None or sales_record is None:
            print(f"Skipping {test_case} - Error loading files")
            continue

        # Convert product list to a dictionary
        price_catalogue = {
            item["title"]: item["price"] for item in price_catalogue_list
        }

        # Compute total sales
        total_cost, _ = compute_total_sales(
            price_catalogue, sales_record
        )

        elapsed_time = time.time() - start_time
        print(
            f"{test_case} Total: ${total_cost:.2f} "
            f"(Processed in {elapsed_time:.4f}s)"
        )

        # Store results
        results.append(f"{test_case}\t{total_cost:.2f}")

    # Write results to file
    os.makedirs("results", exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as result_file:
        result_file.write("TOTAL\n")
        result_file.write("\n".join(results) + "\n")


if __name__ == "__main__":
    process_test_cases()
