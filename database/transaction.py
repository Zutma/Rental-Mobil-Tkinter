from database.connection import create_db_connection

def get_all_transactions(search=""):
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    q = """SELECT tr.id, cust.name AS customer_name, cust.id AS customer_id,
           CONCAT(b.name,' ',t.name,' - ',c.plate_number) AS car_label, c.id AS car_id,
           tr.pickup_date, tr.return_date, tr.guarantee_item, tr.total_price, tr.status, tr.payment_method
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
    cursor.execute("""SELECT c.id, c.rental_price, CONCAT(b.name,' ',t.name,' - ',c.plate_number) AS label
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
    cursor.execute("""SELECT c.id, c.rental_price, CONCAT(b.name,' ',t.name,' - ',c.plate_number) AS label
                      FROM cars c JOIN types t ON c.type_id=t.id JOIN brands b ON t.brand_id=b.id
                      WHERE c.id=%s""", (car_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def add_transaction(customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status, payment_method):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO transactions (customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status, payment_method)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status, payment_method))
    conn.commit()
    cursor.close()
    conn.close()

def update_transaction(trans_id, customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status, payment_method):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE transactions SET customer_id=%s, car_id=%s, pickup_date=%s, return_date=%s,
           guarantee_item=%s, total_price=%s, status=%s, payment_method=%s WHERE id=%s""",
        (customer_id, car_id, pickup_date, return_date, guarantee_item, total_price, status, payment_method, trans_id))
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