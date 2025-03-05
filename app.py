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
    """Returns all expenses (to be implemented)."""
    return jsonify({"message": "This endpoint will return expenses."})



@app.route("/add_expense", methods=["POST"])
def add_expense():
    """Adds a new expense (to be implemented)."""
    return jsonify({"message": "This endpoint will add an expense."})

@app.route("/edit_expense", methods=["POST"])
def edit_expense():
    """Edits an existing expense (to be implemented)."""
    return jsonify({"message": "This endpoint will edit an expense."})

@app.route("/delete_expense", methods=["POST"])
def delete_expense():
    """Deletes an expense (to be implemented)."""
    return jsonify({"message": "This endpoint will delete an expense."})


@app.route("/expense_summary", methods=["GET"])
def expense_summary():
    """Returns the expense summary (to be implemented)."""
    return jsonify({"message": "This endpoint will return expense summary."})


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
