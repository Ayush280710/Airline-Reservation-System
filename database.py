import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'airline.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_db()
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_no TEXT NOT NULL UNIQUE,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure TEXT NOT NULL,
        arrival TEXT NOT NULL,
        base_price INTEGER NOT NULL,
        duration TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pnr TEXT NOT NULL UNIQUE,
        user_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        travel_date TEXT NOT NULL,
        passenger_count INTEGER NOT NULL,
        travel_class TEXT NOT NULL,
        total_price INTEGER NOT NULL,
        payment_method TEXT,
        payment_status TEXT NOT NULL DEFAULT 'Pending',
        status TEXT NOT NULL DEFAULT 'Confirmed',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(flight_id) REFERENCES flights(id)
    );

    CREATE TABLE IF NOT EXISTS passengers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        seat_no TEXT NOT NULL,
        FOREIGN KEY(booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
        UNIQUE(booking_id, seat_no)
    );

    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL UNIQUE,
        method TEXT NOT NULL,
        transaction_ref TEXT NOT NULL,
        amount INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Paid',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(booking_id) REFERENCES bookings(id) ON DELETE CASCADE
    );
    ''')

    flights = [
        ('HA101', 'Delhi', 'Mumbai', '09:00 AM', '11:15 AM', 8499, '2h 15m'),
        ('HA204', 'Delhi', 'Dubai', '01:30 PM', '05:45 PM', 23999, '4h 15m'),
        ('HA305', 'Mumbai', 'London', '07:45 PM', '05:30 AM', 52999, '10h 45m'),
        ('HA410', 'Bengaluru', 'Singapore', '11:15 AM', '05:20 PM', 28999, '5h 05m'),
        ('HA512', 'Delhi', 'Paris', '10:00 PM', '06:45 AM', 47999, '8h 45m'),
        ('HA620', 'Delhi', 'New York', '09:30 PM', '06:00 AM', 68999, '14h 30m'),
        ('HA731', 'Delhi', 'Tokyo', '08:10 PM', '07:00 AM', 55999, '9h 50m'),
        ('HA845', 'Mumbai', 'Dubai', '06:20 PM', '08:15 PM', 21999, '3h 55m'),
    ]

    conn.executemany('''
        INSERT OR IGNORE INTO flights
        (flight_no, source, destination, departure, arrival, base_price, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', flights)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print(f'Database ready: {DB_PATH}')
