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