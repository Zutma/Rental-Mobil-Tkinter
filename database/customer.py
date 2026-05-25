from database.connection import create_db_connection

def get_all_customers(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    q = "SELECT * FROM customers"
    if search:
        q += " WHERE nik LIKE %s OR name LIKE %s OR phone LIKE %s OR address LIKE %s"
        s = f"%{search}%"
        cursor.execute(q + " ORDER BY id", (s, s, s, s))
    else:
        cursor.execute(q + " ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_customer(nik, name, phone, address):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (nik, name, phone, address) VALUES (%s,%s,%s,%s)", (nik, name, phone, address))
    conn.commit()
    cursor.close()
    conn.close()

def update_customer(cust_id, nik, name, phone, address):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET nik=%s, name=%s, phone=%s, address=%s WHERE id=%s", (nik, name, phone, address, cust_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_customer(cust_id):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=%s", (cust_id,))
    conn.commit()
    cursor.close()
    conn.close()