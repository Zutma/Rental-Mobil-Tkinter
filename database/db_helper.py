from database.setup_database import create_db_connection

def authenticate(username, password):
    conn = create_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_dashboard_stats():
    conn = create_db_connection()
    if not conn: return {"mobil": 0, "pelanggan": 0, "transaksi": 0, "user": 0}
    cursor = conn.cursor()
    stats = {}
    for key, table in [("mobil","cars"),("pelanggan","customers"),("transaksi","transactions"),("user","users")]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[key] = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return stats

# ==================== BRANDS & TYPES ====================

def get_brands():
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
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

# ==================== CARS ====================

def get_all_cars(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    q = """SELECT c.id, c.plate_number, b.name AS brand, t.name AS type, c.color, c.year,
           c.rental_price, c.status, c.type_id, t.brand_id
           FROM cars c
           JOIN types t ON c.type_id = t.id
           JOIN brands b ON t.brand_id = b.id"""
    if search:
        q += " WHERE c.plate_number LIKE %s OR b.name LIKE %s OR t.name LIKE %s OR c.color LIKE %s"
        s = f"%{search}%"
        cursor.execute(q + " ORDER BY c.id", (s, s, s, s))
    else:
        cursor.execute(q + " ORDER BY c.id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_car(type_id, plate_number, color, year, rental_price, status):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cars (type_id, plate_number, color, year, rental_price, status) VALUES (%s,%s,%s,%s,%s,%s)",
        (type_id, plate_number, color, year, rental_price, status))
    conn.commit()
    cursor.close()
    conn.close()

def update_car(car_id, type_id, plate_number, color, year, rental_price, status):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cars SET type_id=%s, plate_number=%s, color=%s, year=%s, rental_price=%s, status=%s WHERE id=%s",
        (type_id, plate_number, color, year, rental_price, status, car_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_car(car_id):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id=%s", (car_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ==================== CUSTOMERS ====================

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

# ==================== TRANSACTIONS ====================

def get_all_transactions(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    q = """SELECT tr.id, cust.name AS customer_name, cust.id AS customer_id,
           CONCAT(b.name,' ',t.name,' - ',c.plate_number) AS car_label, c.id AS car_id,
           tr.pickup_date, tr.return_date, tr.guarantee_item, tr.total_price, tr.status
           FROM transactions tr
           JOIN customers cust ON tr.customer_id = cust.id
           JOIN cars c ON tr.car_id = c.id
           JOIN types t ON c.type_id = t.id
           JOIN brands b ON t.brand_id = b.id"""
    if search:
        q += " WHERE cust.name LIKE %s OR c.plate_number LIKE %s OR b.name LIKE %s"
        s = f"%{search}%"
        cursor.execute(q + " ORDER BY tr.id", (s, s, s))
    else:
        cursor.execute(q + " ORDER BY tr.id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_available_cars():
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT c.id, CONCAT(b.name,' ',t.name,' - ',c.plate_number) AS label
                      FROM cars c JOIN types t ON c.type_id=t.id JOIN brands b ON t.brand_id=b.id
                      WHERE c.status='available' ORDER BY b.name""")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_car_by_id(car_id):
    conn = create_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT c.id, CONCAT(b.name,' ',t.name,' - ',c.plate_number) AS label
                      FROM cars c JOIN types t ON c.type_id=t.id JOIN brands b ON t.brand_id=b.id
                      WHERE c.id=%s""", (car_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def add_transaction(customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO transactions (customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status)
           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status))
    conn.commit()
    cursor.close()
    conn.close()

def update_transaction(trans_id, customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE transactions SET customer_id=%s, car_id=%s, pickup_date=%s, return_date=%s,
           guarantee_item=%s, total_price=%s, status=%s WHERE id=%s""",
        (customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status, trans_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_transaction(trans_id):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=%s", (trans_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ==================== USERS ====================

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
