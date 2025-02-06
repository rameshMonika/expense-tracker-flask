from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "expenses.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"categories": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", categories=data["categories"])

@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    data = load_data()
    return jsonify(data)

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = load_data()
    category = request.form.get("category")
    amount = request.form.get("amount")
    description = request.form.get("description", "")
    
    if category not in data["categories"]:
        return jsonify({"error": "Category does not exist"}), 404
    
    if not amount.isnumeric():
        return jsonify({"error": "Invalid expense amount"}), 400
    
    amount = float(amount)
    data["categories"][category]["expenses"].append({"amount": amount, "description": description})
    save_data(data)
    return jsonify({"message": "Expense added successfully"})

@app.route("/edit_expense", methods=["POST"])
def edit_expense():
    data = load_data()
    category = request.form.get("category")
    old_description = request.form.get("old_description")
    new_description = request.form.get("new_description")
    new_amount = request.form.get("new_amount")
    
    if category not in data["categories"]:
        return jsonify({"error": "Category does not exist"}), 404
    
    for expense in data["categories"][category]["expenses"]:
        if expense["description"] == old_description:
            expense["description"] = new_description
            expense["amount"] = float(new_amount)
            save_data(data)
            return jsonify({"message": "Expense updated successfully"})
    
    return jsonify({"error": "Expense not found"}), 404

@app.route("/delete_expense", methods=["POST"])
def delete_expense():
    data = load_data()
    category = request.form.get("category")
    description = request.form.get("description")

    if category not in data["categories"]:
        return jsonify({"error": "Category does not exist"}), 404

    # Filter out only the selected expense
    updated_expenses = [
        exp for exp in data["categories"][category]["expenses"]
        if exp["description"] != description
    ]

    if len(updated_expenses) == len(data["categories"][category]["expenses"]):
        return jsonify({"error": "Expense not found"}), 404

    data["categories"][category]["expenses"] = updated_expenses
    save_data(data)

    return jsonify({"message": "Expense deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)