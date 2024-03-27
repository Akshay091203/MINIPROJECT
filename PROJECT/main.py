from flask import Flask, render_template, request
import pandas as pd
from io import StringIO  # For handling CSV data in memory
import os  # For handling file paths

# Function to calculate support and confidence (same as before)
def calculate_support(itemset, transactions):
    """
    Calculates the support of an itemset within a set of transactions.
    """
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)


def calculate_confidence(item_A, item_B, transactions):
    """
    Calculates the confidence of a rule (item_A -> item_B) based on transactions.
    """
    support_A = calculate_support({item_A}, transactions)
    support_AB = calculate_support({item_A, item_B}, transactions)

    confidence = support_AB / support_A if support_A > 0 else 0
    return confidence


# Function to read CSV data
def read_csv_data(data_path):
    try:
        df = pd.read_csv(data_path)
        return df["Items"].str.split(", ").tolist()
    except FileNotFoundError:
        print(f"Error: File '{data_path}' not found.")
        return []


app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))  # Specify template folder path


@app.route("/", methods=["GET"])
def index():
    # Fetch data from CSV and extract unique items
    data = read_csv_data("store_data_food.csv")  # Replace with your CSV reading function
    unique_items = set(item for transaction in data for item in transaction)

    return render_template("index.html", unique_items=unique_items)


@app.route("/analyze", methods=["POST"])
def analyze():
    item_A = request.form["item_A"]
    item_B = request.form["item_B"]

    data = read_csv_data("store_data_food.csv")  # Replace with your CSV reading function
    transactions = data

    support = calculate_support({item_A, item_B}, transactions)
    confidence = calculate_confidence(item_A, item_B, transactions)

    return render_template("result.html", item_A=item_A, item_B=item_B, support=support, confidence=confidence)


if __name__ == "__main__":
    app.run(debug=True)
