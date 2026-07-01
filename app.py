from flask_login import LoginManager, current_user
from database.queries.users import get_user_by_id
from user import User

from flask import Flask, render_template, flash, redirect, url_for
from routes.auth_routes import auth
from routes.api_routes import api
from database.db import init_database
from database.config import SECRET_KEY
from seed import seed




app = Flask(__name__)

# Set the secret key for session management and CSRF protection (required by Flask-Login)
app.secret_key = SECRET_KEY 

# Create the LoginManager instance that will handle authentication
login_manager = LoginManager()
# Attach the LoginManager to the Flask app
login_manager.init_app(app)
# Set the redirect destination for unauthenticated users hitting @login_required routes
login_manager.login_view = "auth.login_page"

# Register this function as the user loader — Flask-Login calls it on every request
@login_manager.user_loader
def load_user(user_id):
    # Query the DB for the user with this ID (extracted from the session cookie)
    user_data = get_user_by_id(user_id)
    # If the user exists, return a User object so current_user is available in routes
    if user_data:
        return User(id=user_data["id"], role=user_data["role"])
    # If no user found, return None — Flask-Login treats this as logged out
    return None


app.register_blueprint(auth)  # Register the authentication routes
# Register the API routes with the /api prefix for all routes in that blueprint
app.register_blueprint(api)  #

init_database() 
seed()  # Seed the database with default data (admin user, demo user, categories)

@app.route("/app/")
def app_page():
    if current_user.role != "user":
        flash("Access denied. Users only.")
        return redirect(url_for("auth.login_page"))
    return render_template("index.html")


# Run this function automatically after every request Flask handles
@app.after_request
def add_no_cache_headers(response):
    # Tell the browser never to store or cache the response
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    # Older HTTP/1.0 browsers — also tell them not to cache
    response.headers["Pragma"] = "no-cache"
    # Set the expiry date to the past, forcing the browser to treat the response as stale
    response.headers["Expires"] = "0"
    # Return the modified response with the new headers attached
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5001)
