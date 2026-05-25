from database.connection import create_db_connection

def authenticate(username, password):
    conn = create_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user