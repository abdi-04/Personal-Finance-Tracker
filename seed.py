from datetime import date
from database.db import get_connection
from database.queries.users import get_user_by_email, create_user


def admin():
    email = "admin@financetracker.com"
    password = "admin1234"
    firstname = "Admin"
    lastname = "User"

    if get_user_by_email(email):
        print(f"Admin {email} already exists, skipping.")
        return

    create_user(
        email=email,
        password=password,
        firstname=firstname,
        lastname=lastname,
        role="admin"
    )

    print(f"Default admin created: {email} / {password}")

def demo_user():
    email = "demo@financetracker.com"
    password = "demo1234"
    firstname = "Demo"
    lastname = "User"

    if get_user_by_email(email):
        print(f"User {email} already exists, skipping.")
        return

    create_user(email, password, firstname, lastname)

def seed_categories():
    conn = get_connection()
    cursor = conn.cursor()

    categories = [
        ("Entertainment", "expense"),
        ("Food", "expense"),
        ("Income", "income"),
        ("Other", "expense"),
        ("Rent", "expense"),
        ("Transport", "expense"),
    ]

    try:
        for name, type_ in categories:
            cursor.execute(
                "INSERT IGNORE INTO categories (name, type) VALUES (%s, %s)",
                (name, type_)
            )

        conn.commit()

    finally:
        cursor.close()
        conn.close()


def seed_budgets():
    demo = get_user_by_email("demo@financetracker.com")
    if not demo:
        print("Demo user not found, skipping budget seed.")
        return

    user_id = demo["id"]  

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT COUNT(*) FROM budgets WHERE user_id = %s", (user_id,))

    unique = None
    for r in cursor:
        unique = r[0]
    
    if unique > 0:
        print(f"Budgets already seeded for {user_id}, skipping.")
        cursor.close()
        conn.close()
        return

    # Get category IDs by name
    cursor.execute("SELECT id, name FROM categories")
    
    #categories = {name: cid for cid, name in cursor.fetchall()}

    categories = {}

    rows = []
    for row in cursor:
        rows.append(row)
    
    for row in rows:
        cid = row[0]
        name = row[1]

        categories[name] = cid


    budgets = [
        (categories["Food"],          4000.00),
        (categories["Rent"],         6000.00),
        (categories["Transport"],     340.00),
        (categories["Entertainment"], 389.00),
        (categories["Other"],         1000.00),
    ]

    first_of_month = date.today().replace(day=1)

    try:
        for category_id, amount in budgets:
            cursor.execute("""
                INSERT IGNORE INTO budgets (user_id, category_id, amount, month)
                VALUES (%s, %s, %s, %s)
            """, (user_id, category_id, amount, first_of_month))
        conn.commit()
        print(f"Budgets seeded for {user_id}.")
    finally:
        cursor.close()
        conn.close()



def seed_transactions():

    demo = get_user_by_email("demo@financetracker.com")
    if not demo:
        print("Demo user not found, skipping transaction seed.")
        return
    
    user_id = demo["id"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id = %s", (user_id,))

    unique = None

    for r in cursor:
        unique = r[0]
    
    if unique > 0:
        print(f"Transactions already seeded for {user_id}, skipping.")
        cursor.close()
        conn.close()
        return

    cursor.execute("SELECT id, name FROM categories")
    
    categories = {}

    rows = []
    for row in cursor:
        rows.append(row)
    
    for row in rows:
        cid = row[0]
        name = row[1]

        categories[name] = cid

    transactions = [
    (categories["Food"], 124.50, "2021-01-03", "Weekly groceries"),
    (categories["Rent"], 1650.00, "2021-01-01", "Apartment rent"),
    (categories["Transport"], 89.00, "2021-01-07", "Train ticket"),
    (categories["Entertainment"], 299.00, "2021-01-12", "Concert ticket"),
    (categories["Other"], 450.00, "2021-01-18", "New headphones"),
    (categories["Income"], 12500.00, "2021-01-25", "Monthly salary"),

    (categories["Food"], 98.20, "2021-02-04", "Supermarket shopping"),
    (categories["Rent"], 1650.00, "2021-02-01", "Apartment rent"),
    (categories["Transport"], 650.00, "2021-02-10", "Car fuel"),
    (categories["Entertainment"], 149.00, "2021-02-14", "Cinema night"),
    (categories["Other"], 799.00, "2021-02-22", "Winter jacket"),
    (categories["Income"], 12750.00, "2021-02-25", "Monthly salary"),

    (categories["Food"], 135.40, "2022-03-02", "Groceries"),
    (categories["Rent"], 1700.00, "2022-03-01", "Apartment rent"),
    (categories["Transport"], 45.00, "2022-03-05", "Bus pass"),
    (categories["Entertainment"], 599.00, "2022-03-11", "Gaming subscription"),
    (categories["Other"], 1200.00, "2022-03-19", "Phone repair"),
    (categories["Income"], 13000.00, "2022-03-25", "Monthly salary"),

    (categories["Food"], 87.90, "2023-04-08", "Bakery and coffee"),
    (categories["Rent"], 1750.00, "2023-04-01", "Apartment rent"),
    (categories["Transport"], 110.00, "2023-04-09", "Taxi ride"),
    (categories["Entertainment"], 249.00, "2023-04-17", "Museum visit"),
    (categories["Other"], 349.00, "2023-04-23", "Household supplies"),
    (categories["Income"], 13250.00, "2023-04-25", "Monthly salary"),

    (categories["Food"], 210.75, "2024-05-20", "Restaurant dinner"),
    (categories["Rent"], 1800.00, "2024-05-01", "Apartment rent"),
    (categories["Transport"], 95.00, "2024-05-06", "Train ticket"),
    (categories["Entertainment"], 399.00, "2024-05-15", "Theater show"),
    (categories["Other"], 650.00, "2024-05-21", "Sports equipment"),
    (categories["Income"], 13500.00, "2024-05-25", "Monthly salary"),

    (categories["Food"], 189.00, "2025-06-13", "Takeaway dinner"),
    (categories["Rent"], 1850.00, "2025-06-01", "Apartment rent"),
    (categories["Transport"], 120.00, "2025-06-08", "Taxi ride"),
    (categories["Entertainment"], 699.00, "2025-06-17", "Festival ticket"),
    (categories["Other"], 899.00, "2025-06-22", "New office chair"),
    (categories["Income"], 14000.00, "2025-06-25", "Monthly salary"),
    ]

    try:
        for category_id, amount, date_, description in transactions:
            cursor.execute("""
                INSERT INTO transactions (user_id, category_id, amount, date, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, category_id, amount, date_, description))
        conn.commit()
        print(f"Transactions seeded for {user_id}.")
    finally:
        cursor.close()
        conn.close()

def seed_goals():
    demo = get_user_by_email("demo@financetracker.com")
    if not demo:
        print("Demo user not found, skipping goals seed.")
        return
    user_id = demo["id"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM savings_goals
        WHERE user_id = %s
    """, (user_id,))

    unique = None

    for row in cursor:
        unique = row[0]
        break
    if unique > 0:
        print(f"Savings goals already seeded for {user_id}, skipping.")
        cursor.close()
        conn.close()
        return

    goals = [
        ("Emergency Fund", 1000.00),
        ("Vacation", 2000.00),
        ("New Laptop", 2000.00),
        ("New Phone", 1000.00),
        ("New Car", 10000.00),
    ]       
    try:
        for title, target_amount in goals:
            cursor.execute("""
                INSERT INTO savings_goals (user_id, title, target_amount, status)
                VALUES (%s, %s, %s, 'active')
            """, (user_id, title, target_amount))
        conn.commit()
        print(f"Savings goals seeded for {user_id}.")
    finally:
        cursor.close()
        conn.close()



def seed():
    admin()
    demo_user()
    seed_categories()
    seed_budgets()
    seed_transactions()
    seed_goals()

