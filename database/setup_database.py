import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_rental_mobil"
        )
        return conn
    except Error as e:
        print(f"Gagal konek ke database: {e}")
        return None

def setup_all_tables():
    conn = create_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # Daftar query untuk membuat tabel (Urutan sangat menentukan!)
    tables = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                password VARCHAR(255),
                role ENUM('admin', 'petugas') DEFAULT 'admin'
            )
        """,
        "brands": """
            CREATE TABLE IF NOT EXISTS brands (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """,
        "types": """
            CREATE TABLE IF NOT EXISTS types (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand_id INT,
                name VARCHAR(100) NOT NULL,
                FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
            )
        """,
        "cars": """
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type_id INT,
                plate_number VARCHAR(20) UNIQUE NOT NULL,
                color VARCHAR(50),
                year INT,
                status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
                FOREIGN KEY (type_id) REFERENCES types(id) ON DELETE CASCADE
            )
        """,
        "customers": """
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nik VARCHAR(16) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                address TEXT
            )
        """,
        "transactions": """
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                car_id INT,
                pickup_date DATE,
                return_date DATE,
                actual_return_date DATE NULL,
                guarantee_item VARCHAR(255),
                total_price DECIMAL(12, 2),
                status ENUM('booked', 'on_going', 'finished', 'cancelled') DEFAULT 'booked',
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (car_id) REFERENCES cars(id)
            )
        """,
        "fines": """
            CREATE TABLE IF NOT EXISTS fines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_id INT,
                amount DECIMAL(12, 2),
                description TEXT,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
            )
        """,
        "payments": """
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_id INT,
                payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                amount DECIMAL(12, 2),
                method VARCHAR(50),
                FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
            )
        """
    }

    # Jalankan pembuatan tabel satu per satu
    for table_name, query in tables.items():
        try:
            cursor.execute(query)
            print(f"Tabel '{table_name}' siap!")
        except Error as e:
            print(f"Gagal membuat tabel {table_name}: {e}")

    conn.commit() # Simpan perubahan
    cursor.close()
    conn.close()
    print("\n--- SEMUA TABEL BERHASIL DIBUAT ---")

if __name__ == "__main__":
    setup_all_tables()