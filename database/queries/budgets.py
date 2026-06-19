from database.db import get_connection
from datetime import date


def get_budget_with_spending(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # This query fetches the user's budgets for the current month 
    # along with the total spent amount for each budget category.

    # Execute an SQL query to fetch:
    # - all budgets belonging to the user
    # - the category name for each budget
    # - the total amount spent in that category during the same month
    cursor.execute("""
        SELECT 
            b.id,
            b.amount AS budget_amount,
            c.name AS category_name,

            IFNULL(SUM(
                CASE 
                    WHEN tc.type = 'expense' THEN t.amount 
                    ELSE 0
                END
            ), 0) AS spent

        FROM budgets b

        JOIN categories c ON b.category_id = c.id

        LEFT JOIN transactions t 
            ON t.category_id = b.category_id
            AND t.user_id = b.user_id
            AND MONTH(t.date) = MONTH(b.month)
            AND YEAR(t.date) = YEAR(b.month)

        LEFT JOIN categories tc ON t.category_id = tc.id

        WHERE b.user_id = %s

        GROUP BY b.id
    """, (user_id,))

    data = []
    for row in cursor:
        data.append(row)

    cursor.close()
    conn.close()
    return data


def save_budget(user_id, category_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    today = date.today()
    first_day_of_month = today.replace(day=1)

    # Check if exists
    cursor.execute("""
        SELECT id FROM budgets 
        WHERE user_id=%s AND category_id=%s AND month=%s
    """, (user_id, category_id, first_day_of_month))

    existing = None
    for row in cursor:
        existing = row
        break

    if existing:
        # Update instead
        cursor.execute("""
            UPDATE budgets SET amount=%s
            WHERE user_id=%s AND category_id=%s AND month=%s
        """, (amount, user_id, category_id, first_day_of_month))
    else:
        cursor.execute("""
            INSERT INTO budgets (user_id, category_id, amount, month)
            VALUES (%s, %s, %s, %s)
        """, (user_id, category_id, amount, first_day_of_month))

    conn.commit()
    cursor.close()
    conn.close()


def delete_budget(budget_id, user_id):
    """Delete a budget entry — user_id ensures users can only delete their own"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM budgets WHERE id = %s AND user_id = %s",
        (budget_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()



def update_budget(budget_id, user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE budgets SET amount = %s WHERE id = %s AND user_id = %s",
        (amount, budget_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

