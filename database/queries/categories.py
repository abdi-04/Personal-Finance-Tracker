from database.db import get_connection

def get_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, type 
        FROM categories 
        ORDER BY name
    """)

    rows = []
    for row in cursor:
        rows.append({
            "id": row["id"],
            "name": row["name"],
            "type": row["type"]
        })

    cursor.close()
    conn.close()

    return rows



def save_category(name, type_):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO categories (name, type) VALUES (%s, %s)",
        (name, type_)
    )

    conn.commit()
    cursor.close()
    conn.close()

    

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM categories WHERE id = %s",
        (category_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_category(category_id, name, type_):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categories SET name = %s, type = %s WHERE id = %s",
        (name, type_, category_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

