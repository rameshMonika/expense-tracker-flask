# Import necessary libraries
from flask import Flask, request, render_template, jsonify
import json
import os
import random  #  Random numbers
import shutil  #  Copy files
import math  #  Math functions

# 🎞️ Variables & Multiple Assignments
DATA_FILE, CATEGORY = "expenses.json", "sports"

#  Create Flask App
app = Flask(__name__)



def save_data(data):
    """Saves expense data to a JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

#  File Detection & Handling
def load_data():
    """Loads expense data from a JSON file or initializes it if not found."""
    if os.path.exists(DATA_FILE): 
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return {"categories": {CATEGORY: {"expenses": []}}}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    """Returns all expenses under the 'sports' category."""
    data = load_data()
    return jsonify(data["categories"][CATEGORY]["expenses"])



@app.route("/add_expense", methods=["POST"])
def add_expense():
    """Adds a new expense."""
    data = load_data()
   
    # User Input & Type Casting
    amount = request.form.get("amount")
    description = request.form.get("description", "").strip()

    print(amount)

    # Check if amount is a valid float
    try:
        amount = float(amount)
        if amount < 0:  # Optional: Prevent negative values
            return jsonify({"error": "Amount cannot be negative"}), 400
    except ValueError:
        print("Invalid expense amount")
        return jsonify({"error": "Invalid expense amount"}), 400

    # Append New Expense
    data["categories"][CATEGORY]["expenses"].append({"amount": amount, "description": description})
    save_data(data)

    return jsonify({"message": "Expense added successfully"})



@app.route("/edit_expense", methods=["PUT"])
def edit_expense():
    """Edits an existing expense."""
    data = load_data()
   
    # Variable Scope
    old_description = request.form.get("old_description", "").strip()
    new_description = request.form.get("new_description", "").strip()
    new_amount = request.form.get("new_amount", "").strip()

    expenses_list = data["categories"][CATEGORY]["expenses"]

    # ➰ For Loop (Iterate through expenses)
    for expense in expenses_list:
        if expense["description"] == old_description:
            #  String Slicing (Just an example)
            expense["description"] = new_description
            expense["amount"] = float(new_amount)

            save_data(data)
            return jsonify({"message": "Expense updated successfully"})

    return jsonify({"error": "Expense not found"}), 404


@app.route("/delete_expense", methods=["DELETE"])
def delete_expense():
    """Deletes an expense."""
    data = load_data()
    request_data = request.get_json()
    description = request_data.get("description", "").strip()

    expenses_list = data["categories"][CATEGORY]["expenses"]
    

    updated_expenses = [exp for exp in expenses_list if exp["description"] != description]

    if len(updated_expenses) == len(expenses_list):
        return jsonify({"error": "Expense not found"}), 404

    data["categories"][CATEGORY]["expenses"] = updated_expenses
    save_data(data)

    return jsonify({"message": "Expense deleted successfully"})


@app.route("/expense_summary", methods=["GET"])
def expense_summary():
    """Returns the limit and total expenses for the sports category."""
    data = load_data()
    category_data = data["categories"].get(CATEGORY, {})
    
    limit = category_data.get("limit", 0)
    total = sum(expense["amount"] for expense in category_data.get("expenses", []))

    return jsonify({"limit": limit, "total_expense": total})

#  File Management Operations
@app.route("/backup", methods=["GET"])
def backup_file():
    """Creates a backup of the expenses.json file."""
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, f"{DATA_FILE}.backup")
        return jsonify({"message": "Backup created successfully."})
    return jsonify({"error": "No file to back up."}), 404

if __name__ == "__main__":

    def start_server(*args):
        """Starts the Flask server."""
        app.run(*args, debug=True)

    start_server()
