import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file into environment variables

DB_CONFIG = {
    "host": os.getenv("db_host"),
    "user": os.getenv("db_user"),
    "password": os.getenv("db_password"),
    "database": os.getenv("db_name"),
}

SECRET_KEY = os.getenv("secret_key")