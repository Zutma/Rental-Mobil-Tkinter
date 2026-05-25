from database.connection import create_db_connection

def get_all_users(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    q = "SELECT id, name, role FROM users"
    if search:
        q += " WHERE name LIKE %s OR role LIKE %s"
        s = f"%{search}%"
        cursor.execute(q + " ORDER BY id", (s, s))
    else:
        cursor.execute(q + " ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_user(name, password, role):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, password, role) VALUES (%s,%s,%s)", (name, password, role))
    conn.commit()
    cursor.close()
    conn.close()

def update_user(user_id, name, password, role):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    if password:
        cursor.execute("UPDATE users SET name=%s, password=%s, role=%s WHERE id=%s", (name, password, role, user_id))
    else:
        cursor.execute("UPDATE users SET name=%s, role=%s WHERE id=%s", (name, role, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()