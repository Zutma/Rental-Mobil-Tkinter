from database.connection import create_db_connection

def get_all_types(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    q = """SELECT t.id, t.name, t.brand_id, b.name AS brand_name
           FROM types t JOIN brands b ON t.brand_id = b.id"""
    if search:
        q += " WHERE t.name LIKE %s OR b.name LIKE %s"
        s = f"%{search}%"
        cursor.execute(q + " ORDER BY b.name, t.name", (s, s))
    else:
        cursor.execute(q + " ORDER BY b.name, t.name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_types_by_brand(brand_id):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM types WHERE brand_id=%s ORDER BY name", (brand_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_type(brand_id, name):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO types (brand_id, name) VALUES (%s, %s)", (brand_id, name))
    conn.commit()
    type_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return type_id

def update_type(type_id, brand_id, name):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("UPDATE types SET brand_id=%s, name=%s WHERE id=%s", (brand_id, name, type_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_type(type_id):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM types WHERE id=%s", (type_id,))
    conn.commit()
    cursor.close()
    conn.close()