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

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    """Returns all expenses under the 'sports' category."""
    data = load_data()
    return jsonify(data["categories"][CATEGORY]["expenses"])

#  File Detection & Handling
def load_data():
    """Loads expense data from a JSON file or initializes it if not found."""
    if os.path.exists(DATA_FILE): 
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return {"categories": {CATEGORY: {"expenses": []}}}

@app.route("/expense_summary", methods=["GET"])
def expense_summary():
    """Returns the limit and total expenses for the sports category."""
    data = load_data()
    category_data = data["categories"].get(CATEGORY, {})
    
    limit = category_data.get("limit", 0)
    total = sum(expense["amount"] for expense in category_data.get("expenses", []))

    return jsonify({"limit": limit, "total_expense": total})

@app.route("/add_expense", methods=["POST"])
def add_expense():
    """Adds a new expense."""
    data = load_data()
    
    # User Input & Type Casting
    amount = request.form.get("amount")
    description = request.form.get("description", "").strip()

    if not amount or not amount.isnumeric():
        return jsonify({"error": "Invalid expense amount"}), 400
    
    amount = float(amount)  # 
    #  Lists & Append New Expense
    data["categories"][CATEGORY]["expenses"].append({"amount": amount, "description": description})
    save_data(data)

    return jsonify({"message": "Expense added successfully"})

@app.route("/edit_expense", methods=["POST"])
def edit_expense():
    """Edits an existing expense."""
    data = load_data()
    
    # 🔬 Variable Scope
    old_description = request.form.get("old_description", "").strip()
    new_description = request.form.get("new_description", "").strip()
    new_amount = request.form.get("new_amount", "").strip()

    expenses_list = data["categories"][CATEGORY]["expenses"]

    # ➰ For Loop (Iterate through expenses)
    for expense in expenses_list:
        if expense["description"] == old_description:
            #  String Slicing (Just an example)
            expense["description"] = new_description[:50] if new_description else expense["description"]
            expense["amount"] = float(new_amount) if new_amount.replace('.', '', 1).isdigit() else expense["amount"]

            save_data(data)
            return jsonify({"message": "Expense updated successfully"})

    return jsonify({"error": "Expense not found"}), 404

@app.route("/delete_expense", methods=["POST"])
def delete_expense():
    """Deletes an expense."""
    data = load_data()
    description = request.form.get("description", "").strip()

    expenses_list = data["categories"][CATEGORY]["expenses"]
    
    # Random Number (Logging)
    print(f"Deleting {description}, Confirmation ID: {random.randint(1000, 9999)}")

    updated_expenses = [exp for exp in expenses_list if exp["description"] != description]

    if len(updated_expenses) == len(expenses_list):
        return jsonify({"error": "Expense not found"}), 404

    data["categories"][CATEGORY]["expenses"] = updated_expenses
    save_data(data)

    return jsonify({"message": "Expense deleted successfully"})



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
