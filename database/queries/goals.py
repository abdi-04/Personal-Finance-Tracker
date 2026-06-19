from database.db import get_connection


def get_goals_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, title, target_amount, status
        FROM savings_goals
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))

    goals = []
    for row in cursor:
        goals.append(row)

    cursor.close()
    conn.close()
    return goals


def save_goal(user_id, title, target_amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO savings_goals
        (user_id, title, target_amount, status)
        VALUES (%s, %s, %s, 'active')
    """, (user_id, title, target_amount))

    conn.commit()
    cursor.close()
    conn.close()


def update_goal(goal_id, user_id, title, target_amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE savings_goals
        SET title = %s,
            target_amount = %s
        WHERE id = %s AND user_id = %s
    """, (title, target_amount, goal_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def update_goal_status(goal_id, user_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE savings_goals
        SET status = %s
        WHERE id = %s AND user_id = %s
    """, (status, goal_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def delete_goal(goal_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM savings_goals
        WHERE id = %s AND user_id = %s
    """, (goal_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()