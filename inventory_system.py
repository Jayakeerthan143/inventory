"""
SRN: PES1UG23CS262

A basic inventory management program that keeps track of stock levels.
This script supports adding, removing, and viewing inventory items,
and saves all data persistently in a JSON file.
"""
# FIX (Pylint: C0114): Added an overall module description.

import json
from datetime import datetime

# Using a global dictionary to maintain inventory data throughout the session.
stock_data = {}


# FIX (Pylint: C0103): Updated function names to follow snake_case convention.
def add_item(item="default", qty=0, logs=None):
    """Adds the given quantity of an item to the inventory."""
    # FIX (Pylint: W0102): Changed default list argument to None to avoid shared state issues.
    if logs is None:
        logs = []

    # FIX: Introduced input validation to prevent type errors.
    if not isinstance(qty, (int, float)):
        print(f"Error: Quantity for '{item}' must be a number.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # FIX (Pylint: C0209): Used f-strings for cleaner and modern string formatting.
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Removes a certain quantity of an item from the inventory."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # FIX (Flake8: E722, Bandit: B110): Avoided bare except; catching only the relevant error type.
    except KeyError:
        print(f"Warning: '{item}' not found in stock, cannot remove it.")


def get_qty(item):
    """Returns the quantity of a given item safely."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads saved stock information from a JSON file."""
    global stock_data
    try:
        # FIX (Pylint: R1732): Used 'with' block for better resource handling.
        # FIX (Pylint: W1514): Added explicit file encoding for compatibility.
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stock_data = {}


def save_data(file="inventory.json"):
    """Writes the current stock data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        # Added indentation for better readability in the saved JSON file.
        json.dump(stock_data, f, indent=4)


def print_data():
    """Displays a summary of all items currently in stock."""
    # FIX (Pylint: C0116): Added missing docstrings to all functions.
    print("\n--- Inventory Report ---")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("-------------------------\n")


def check_low_items(threshold=5):
    """Finds and returns items with stock below a given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


# FIX (Flake8: E302/E305): Ensured proper spacing between top-level functions.
def main():
    """Main function to run and demonstrate the inventory management system."""
    # FIX (Flake8: F401, Pylint: W0611): Removed unused import 'logging'.

    load_data()
    add_item("apple", 10)
    add_item("banana", -2)
    add_item("milk", "five")  # Now handled safely with input validation.
    remove_item("apple", 3)
    remove_item("orange", 1)  # Gracefully handled by catching KeyError.

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    print_data()
    save_data()

    # FIX (Bandit: B307, Pylint: W0123): Removed unsafe 'eval()' usage.
    print("Inventory check completed successfully.")


# Standard Python practice: run main() only when executed directly.
if __name__ == "__main__":
    main()
