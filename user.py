from flask_login import UserMixin


class User(UserMixin): # Inherit from UserMixin to get default implementations of Flask-Login's required user methods
    def __init__(self, id, role=None): # Initialize the User object with an ID and an optional role (e.g., "admin" or "user")
        self.id = id # Store the user's ID (this is what Flask-Login uses to track the user in the session)
        self.role = role # Store the user's role

