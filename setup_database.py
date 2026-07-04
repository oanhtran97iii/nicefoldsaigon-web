import os
import json
import sqlite3

db_path = "/Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/brain.db"
waitlist_path = "/Users/oanhtran97/Desktop/Website/nice-fold-saigon-premium/waitlist.json"

# 1. Create waitlist.json with the requested structure
waitlist_data = {
    "waitlist": [
        {
            "name": "Oanh",
            "phone": "0978900616",
            "service": "Standard Service (24h)",
            "registered_at": "2026-06-29T15:02:00Z"
        }
    ]
}

with open(waitlist_path, "w", encoding="utf-8") as f:
    json.dump(waitlist_data, f, indent=2, ensure_ascii=False)
print("1. Created waitlist.json successfully.")

# 2. Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# 3. Create products table
# CHECK constraint ensures stock_quantity is not null only when product type is 'physical'
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('physical', 'digital', 'service')),
    price REAL NOT NULL,
    description TEXT,
    stock_quantity INTEGER CHECK(type != 'physical' OR stock_quantity IS NOT NULL),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")

# 4. Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE,
    zalo TEXT UNIQUE,
    email TEXT,
    hotel TEXT,
    room TEXT,
    registration_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")

# 5. Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_code TEXT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    order_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
""")

conn.commit()
print("2. Created tables products, customers, and orders successfully.")

# 6. Import data from waitlist.json into customers table (avoiding duplicates)
with open(waitlist_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    waitlist = data.get("waitlist", [])

imported_count = 0
for entry in waitlist:
    name = entry.get("name")
    phone = entry.get("phone")
    registered_at = entry.get("registered_at")
    
    # Check if customer already exists based on phone to prevent duplicate import
    cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute("""
            INSERT INTO customers (name, phone, registration_date)
            VALUES (?, ?, ?)
        """, (name, phone, registered_at))
        imported_count += 1

conn.commit()
print(f"3. Imported {imported_count} customer(s) from waitlist.json into customers table.")

# 7. Verification Summary
print("\n--- DATABASE STATE ---")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print(f"Current tables: {', '.join(tables)}")

cursor.execute("PRAGMA table_info(products);")
print("\nProducts Schema:")
for col in cursor.fetchall():
    print(f" - {col[1]} ({col[2]})")

cursor.execute("SELECT * FROM customers;")
customers = cursor.fetchall()
print(f"\nCustomers list (total {len(customers)}):")
for c in customers:
    print(f" - ID: {c[0]}, Name: {c[1]}, Phone: {c[2]}, Zalo: {c[3]}, RegDate: {c[4]}")

conn.close()
