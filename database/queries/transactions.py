from database.db import get_connection


### Transactions queries ### 

# Get all transactions for a user, including category details
def get_transactions_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Fetch transactions with category details using 
    # LEFT JOIN to include transactions without categories
    cursor.execute(
        """
        SELECT transactions.id, transactions.amount, transactions.description, transactions.date, transactions.image,
               categories.id AS category_id, categories.name AS category_name, categories.type
        FROM transactions
        LEFT JOIN categories ON transactions.category_id = categories.id 
        WHERE transactions.user_id = %s 
        ORDER BY transactions.date DESC, transactions.created_at DESC
        LIMIT 100
        """,
        (user_id,)
    )
    rows = []
    for row in cursor:
        rows.append({
        "id": row["id"],
        "amount": float(row["amount"]),
        "description": row["description"],
        "date": row["date"].isoformat(),
        "image": row["image"],
        "category_id": row["category_id"],
        "category_name": row["category_name"],
        "type": row["type"]
        })
    cursor.close()
    conn.close()
    return rows

# Get a single transaction by ID for a user
def save_transaction(user_id, category_id, amount, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO transactions (user_id, category_id, amount, description, date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, category_id, amount, description, date)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_transaction(transaction_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM transactions WHERE id = %s AND user_id = %s",
        (transaction_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_transaction(transaction_id, user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE transactions SET amount = %s WHERE id = %s AND user_id = %s",
        (amount, transaction_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()



# Update transaction with new category
def update_transaction_image(transaction_id, user_id, filename):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET image = %s
        WHERE id = %s AND user_id = %s
        """,
        (filename, transaction_id, user_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

# Get all transactions with images for a user, including category details
def get_transaction_uploads(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT t.id, t.description, t.image, t.amount, t.date,
               c.name AS category_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = %s AND t.image IS NOT NULL
        ORDER BY t.id DESC
        """,
        (user_id,)
    )

    rows = []
    for r in cursor:
        rows.append({
            "id": r["id"],
            "description": r["description"],
            "image": r["image"],
            "amount": float(r["amount"]),
            "date": r["date"].isoformat(),
            "category_name": r["category_name"]
        })

    cursor.close()
    conn.close()
    return rows
