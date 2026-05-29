from database.connection import create_db_connection

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

def get_rented_cars():
    """Ambil data mobil yang sedang berstatus rented untuk ditampilkan di Dashboard"""
    conn = create_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.plate_number, b.name AS brand, t.name AS type, c.color,
               CONCAT(b.name, ' ', t.name) AS car_name
        FROM cars c
        JOIN types t ON c.type_id = t.id
        JOIN brands b ON t.brand_id = b.id
        WHERE c.status = 'rented'
        ORDER BY b.name, t.name
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
