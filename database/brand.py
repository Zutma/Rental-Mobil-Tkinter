from database.connection import create_db_connection

def get_brands(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    if search:
        cursor.execute("SELECT * FROM brands WHERE name LIKE %s ORDER BY name", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM brands ORDER BY name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_brand(name):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO brands (name) VALUES (%s)", (name,))
    conn.commit()
    brand_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return brand_id

def update_brand(brand_id, name):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("UPDATE brands SET name=%s WHERE id=%s", (name, brand_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_brand(brand_id):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM brands WHERE id=%s", (brand_id,))
    conn.commit()
    cursor.close()
    conn.close()