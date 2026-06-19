from flask import Blueprint, render_template, redirect, url_for, request, flash
from database.queries.users import get_user_by_email, create_user, get_all_users
import bcrypt
from user import User
from flask_login import login_user, logout_user, login_required, current_user
from database.queries.categories import get_categories


auth = Blueprint("auth", __name__)


@auth.route("/admin")
@login_required
def admin_page():

    # Only allow access to this page if the logged-in user has the "admin" role
    if current_user.role != "admin":
        flash("Access denied. Admins only.")
        return redirect(url_for("auth.login_page"))
    
    return render_template(
        "admin.html",
        users=get_all_users(),
        categories=get_categories(),
    )


@auth.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")

    # POST — process the form
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("auth.login_page"))

    user = get_user_by_email(email)

    # Check if user exists and password is correct using bcrypt
    if user and bcrypt.checkpw(password.encode("utf-8"), 
                               user["password_hash"].encode("utf-8")):
        # Create a User object for Flask-Login and log the user in
        #  so current_user can access their ID and role across the app
        user_obj = User(user["id"], user["role"])
        login_user(user_obj)
        if user["role"] == "admin":
            return redirect(url_for("auth.admin_page"))

        return redirect(url_for("app_page"))
    
    # send jwt token to client and store it in local storage or cookie for authentication in future requests
    # jwt_token = create_jwt(user["id"])
    # response = make_response(redirect(url_for("app_page")))
    # response.set_cookie("jwt_token", jwt_token)

    flash("Invalid email or password.", "error")
    return redirect(url_for("auth.login_page"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # POST — process the form
    firstname = request.form.get("firstname", "").strip()
    lastname = request.form.get("lastname", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    confirm = request.form.get("confirm_password", "").strip()

    if not firstname or not lastname or not email or not password or not confirm:
        flash("All fields are required.", "error")
        return redirect(url_for("auth.register"))

    if password != confirm:
        flash("Passwords do not match.", "error")
        return redirect(url_for("auth.register"))

    if len(password) < 8:
        flash("Password must be at least 8 characters.", "error")
        return redirect(url_for("auth.register"))

    if get_user_by_email(email):
        flash("An account with that email already exists.", "error")
        return redirect(url_for("auth.register"))

    create_user(email, password, firstname, lastname)
    flash("Account created! Please log in.", "success")
    return redirect(url_for("auth.login_page"))


## Used for logging out users (both admin and regular users)
@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login_page"))

