# routes/api_routes.py
#
# Defines all API and section-rendering routes for the application.
# Routes are grouped by domain: categories, transactions, budget, goals, users, and settings.
import os
import re
# Used for file type identification
import magic

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from dashboard import get_dashboard_data
from database.queries.budgets import (
    delete_budget, get_budget_with_spending, save_budget, update_budget,
)
from database.queries.categories import (
    delete_category, get_categories, save_category, update_category,
)
from database.queries.goals import (
    delete_goal, get_goals_for_user, save_goal, update_goal,
    update_goal_status,
)
from database.queries.transactions import (
    delete_transaction, get_transaction_uploads, get_transactions_for_user,
    save_transaction, update_transaction, update_transaction_image,
)
from database.queries.users import (
    delete_user, get_all_users, get_user_by_id, update_user_password,
)

# This Blueprint groups all routes defined in this file under the "api" namespace.
api = Blueprint("api", __name__) 




# ---------------------------------------------------------------------------
# Category routes  (admin only)
# ---------------------------------------------------------------------------

# route registers post request from front-end to create a new category in the database. 
@api.route("/categories", methods=["POST"])
@login_required
def save_category_route():

    if current_user.role != "admin":
        return jsonify({"error": "Access denied: Admins only"}), 403

    data = request.get_json()
    name = data.get("name", "").strip()
    type_ = data.get("type")

    if not name or type_ not in ("income", "expense"):
        return jsonify({"error": "Invalid category data"}), 400

    try:
        save_category(name, type_)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/categories/<int:category_id>", methods=["DELETE"])
@login_required
def delete_category_route(category_id):
    if current_user.role != "admin":
        return jsonify({"error": "Access denied: Admins only"}), 403

    delete_category(category_id)
    return "", 204


@api.route("/categories/<int:category_id>", methods=["PUT"])
@login_required
def update_category_route(category_id):
    if current_user.role != "admin":
        return jsonify({"error": "Access denied: Admins only"}), 403

    data = request.get_json()
    name = data.get("name", "").strip()
    type_ = data.get("type")

    if not name or type_ not in ("income", "expense"):
        return jsonify({"error": "Invalid category data"}), 400

    try:
        update_category(category_id, name, type_)
        return "", 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@api.route("/admin/<int:user_id>", methods=["DELETE"])
@login_required
def admin_delete_user_route(user_id):
    """Permanently delete a user account. Requires admin privileges."""

    if current_user.role != "admin":
        return jsonify({"error": "Access denied: Admins only"}), 403

    delete_user(user_id)
    return "", 204




# ---------------------------------------------------------------------------
# Transaction routes
# ---------------------------------------------------------------------------



def sanitize_filename(filename):
    """Strip path components and replace unsafe characters with underscores."""

    # os.path.basename() strips any folder path from the filename.
    # e.g. "../../etc/passwd" becomes just "passwd" — prevents path traversal attacks.
    filename = os.path.basename(filename)

    # re.sub() searches the filename using a regex pattern and replaces matches.
    # This pattern allows only letters, numbers, underscores, dots, and hyphens. All other characters become underscores.
    return re.sub(r"[^\w.\-]", "_", filename) 


# This decorator registers the URL route for this function.
@api.route("/transactions/<int:transaction_id>/receipt", methods=["POST"])
@login_required
def upload_receipt(transaction_id):

    # Fetch all transactions that belong to the currently logged-in user.
    transactions = get_transactions_for_user(current_user.id)

    # Search the user's transactions for the one matching the transaction_id from the URL.
    # If the transaction belongs to a different user, it won't be in the list — so None is returned.
    transaction = None

    for t in transactions:
        if t["id"] == transaction_id:
            transaction = t 
            break

    # If no matching transaction was found (None), stop here and return a 404 error.
    # 404 is the HTTP status code meaning "Not Found".
    if not transaction:
        return jsonify({"error": "Not found"}), 404

    # Check the Content-Length header sent by the client (the file size in bytes).
    # 5 * 1024 * 1024 = 5,242,880 bytes = 5MB.
    # If the file is too large, reject it immediately with HTTP 413 (Payload Too Large).
    # We do this BEFORE reading the file to avoid wasting server memory.
    if request.content_length and request.content_length > 5 * 1024 * 1024:
        return jsonify({"error": "File too large (max 5MB)"}), 413

    # request.files is a dict of all files included in the POST request.
    # We expect a file field named "image". If it's missing, the request is malformed.
    # Return HTTP 400 (Bad Request).
    if "image" not in request.files:
        return jsonify({"error": "No file"}), 400

    # Retrieve the uploaded file object from the request.
    # This is a Flask FileStorage object with properties like .filename and methods like .read() and .save().
    file = request.files["image"]

    # A file field can exist in the request but still be empty (user submitted without selecting a file).
    # file.filename == "" catches that case. Return HTTP 400.
    if not file or file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Read only the first 2048 bytes of the file — enough to detect its true type.
    # We do NOT trust the file extension (e.g. ".jpg") because anyone can rename a file.
    file_bytes = file.read(2048)

    # magic.from_buffer() inspects the raw bytes to determine the real MIME type (media type).
    # e.g. a real JPEG always starts with specific "magic bytes" regardless of its name.
    # mime=True tells the library to return a MIME type string like "image/jpeg".
    mime = magic.from_buffer(file_bytes, mime=True)

    # Rewind the file pointer back to the start (position 0).
    # We read 2048 bytes above, so without this the rest of the file would be missing when we save it.
    file.seek(0)

    # Only allow JPEG and PNG images — reject everything else (PDFs, scripts, executables, etc.).
    # This check uses the MIME type detected from the file contents, not the filename extension.
    if mime not in ("image/jpeg", "image/png"):
        return jsonify({"error": "Invalid file type"}), 400

    # Build a unique, safe filename by combining:
    # - current_user.id: ties the file to its owner
    # - transaction_id: ties the file to the specific transaction
    # - sanitize_filename(file.filename): the cleaned-up original filename
    filename = f"{current_user.id}_{transaction_id}_{sanitize_filename(file.filename)}"

    # Set the directory where uploaded files will be stored.
    upload_dir = "static/uploads"

    # Create the directory if it doesn't already exist.
    os.makedirs(upload_dir, exist_ok=True)

    # Save the uploaded file to disk.
    # os.path.join() safely combines the directory and filename into a full path,
    # handling slashes correctly across different operating systems.
    file.save(os.path.join(upload_dir, filename))

    # Update the database record for this transaction to store the filename.
    # Without this, the file exists on disk but the app has no record of which transaction it belongs to.
    update_transaction_image(transaction_id, current_user.id, filename)

    # Everything succeeded — return HTTP 200 (OK) with a JSON success response.
    return jsonify({"success": True}), 200

# Used by dashboard-chart to display transactions
@api.route("/transactions", methods=["GET"])
@login_required

def transactions_data():
    user_id = current_user.id
    transactions = get_transactions_for_user(user_id)

    return jsonify({"transactions": transactions})

 
@api.route("/transactions", methods=["POST"])
@login_required
def save_transaction_route():
    """Create a new transaction for the current user."""

    data = request.get_json() # retrieve data from js 
    category_id = data.get("category_id")
    amount      = data.get("amount")
    description = data.get("description", "").strip()
    date        = data.get("date")

    if not amount or not date:
        return jsonify({"error": "Amount and date are required"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        # category_id is optional; fall back to None if not provided
        save_transaction(current_user.id, category_id or None, amount, description, date)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/transactions/<int:transaction_id>", methods=["DELETE"])
@login_required
def delete_transaction_route(transaction_id):
    """Delete a transaction belonging to the current user."""

    delete_transaction(transaction_id, current_user.id)
    return "", 204


@api.route("/transactions/<int:transaction_id>", methods=["PUT"])
@login_required
def update_transaction_route(transaction_id):
    """Update the amount on an existing transaction."""

    data   = request.get_json()
    amount = data.get("amount")

    if not amount:
        return jsonify({"error": "Invalid amount"}), 400

    try: 
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    update_transaction(transaction_id, current_user.id, float(amount))
    return "", 204


# ---------------------------------------------------------------------------
# Budget routes
# ---------------------------------------------------------------------------


@api.route("/budget", methods=["POST"])
@login_required
def save_budget_route():
    """Create a new budget entry for a given category."""

    data = request.get_json()
    category_id = data.get("category_id")
    amount = data.get("amount")

    if not category_id or not amount:
        return jsonify({"error": "Missing category_id or amount"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        save_budget(current_user.id, category_id, amount)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/budget/<int:budget_id>", methods=["DELETE"])
@login_required
def delete_budget_route(budget_id):
    """Delete a budget entry belonging to the current user."""

    delete_budget(budget_id, current_user.id)
    return "", 204


@api.route("/budget/<int:budget_id>", methods=["PUT"])
@login_required
def update_budget_route(budget_id):
    """Update the limit amount on an existing budget entry."""

    data   = request.get_json()
    amount = data.get("amount")

    if not amount or float(amount) <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    update_budget(budget_id, current_user.id, float(amount))
    return "", 204


# ---------------------------------------------------------------------------
# Goal routes
# ---------------------------------------------------------------------------

@api.route("/goals", methods=["POST"])
@login_required
def save_goal_route():
    """Create a new savings goal for the current user."""

    data          = request.get_json()
    title         = data.get("title", "").strip()
    target_amount = data.get("target_amount")

    if not title or not target_amount:
        return jsonify({"error": "Missing title or target amount"}), 400

    try:
        target_amount = float(target_amount)
        if target_amount <= 0:
            return jsonify({"error": "Target amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid target amount"}), 400

    save_goal(current_user.id, title, target_amount)
    return jsonify({"success": True}), 200


@api.route("/goals/<int:goal_id>", methods=["PUT"])
@login_required
def update_goal_route(goal_id):
    """Update the title and target amount of an existing goal."""

    data = request.get_json()
    title = data.get("title", "").strip()
    target_amount = data.get("target_amount")
    status = data.get("status")

    if status is not None:
        if status not in ("active", "completed"):
            return jsonify({"error": "Invalid status value"}), 400
        update_goal_status(goal_id, current_user.id, status)
        return "", 204
    

    if not title or not target_amount:
        return jsonify({"error": "Missing title or target amount"}), 400

    try:
        target_amount = float(target_amount)
        if target_amount <= 0:
            return jsonify({"error": "Target amount must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid target amount"}), 400
    
    update_goal_status(goal_id, current_user.id, status)
    update_goal(goal_id, current_user.id, title, target_amount)
    return "", 204


@api.route("/goals/<int:goal_id>", methods=["DELETE"])
@login_required
def delete_goal_route(goal_id):
    """Delete a goal belonging to the current user."""

    delete_goal(goal_id, current_user.id)
    return "", 204



# ---------------------------------------------------------------------------
# Settings 
# ---------------------------------------------------------------------------

@api.route("/settings", methods=["PUT"])
@login_required
def update_password_route():
    """Update the current user's password after validating both fields match."""

    data = request.get_json()
    new_password = data.get("new_password", "").strip()
    confirm_password = data.get("confirm_password", "").strip()

    if not new_password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400

    if new_password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    update_user_password(current_user.id, new_password)
    return jsonify({"success": True}), 200


# ---------------------------------------------------------------------------
# Section HTML routes  (returns rendered Jinja templates for the SPA shell)
# ---------------------------------------------------------------------------

@api.route("/section/<section_name>")
@login_required
def section_html(section_name):
    """
    Render and return the HTML fragment for the requested app section.
    Used by the front-end to swap content without a full page reload.
    """

    user_id = current_user.id

    if section_name == "dashboard":
        return render_template("dashboard.html", **get_dashboard_data(user_id))

    if section_name == "transactions":
        return render_template(
            "transactions.html",
            transactions=get_transactions_for_user(user_id),
            categories=get_categories(),
        )

    if section_name == "budget":
        return render_template(
            "budget.html",
            budget=get_budget_with_spending(user_id),
            categories=get_categories(),
        )

    if section_name == "goals":
        return render_template("goals.html", goals=get_goals_for_user(user_id))

    if section_name == "settings":
        return render_template(
            "settings.html",
            user=get_user_by_id(user_id),
            categories=get_categories(),
            uploads=get_transaction_uploads(user_id),
        )

    if section_name == "admin":

        return render_template(
            "admin.html",
            users=get_all_users(),
            categories=get_categories(),
            current_user_id=user_id,
        )

    return jsonify({"error": "unknown section"}), 404