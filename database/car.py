from database.connection import create_db_connection

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

def update_car_status(car_id, status):
    conn = create_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("UPDATE cars SET status=%s WHERE id=%s", (status, car_id))
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