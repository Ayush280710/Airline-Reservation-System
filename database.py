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
    # ───────────── DOMESTIC ─────────────

    ('HA101', 'Delhi', 'Mumbai', '09:00 AM', '11:15 AM', 8499, '2h 15m'),
    ('HA102', 'Mumbai', 'Delhi', '01:00 PM', '03:10 PM', 8299, '2h 10m'),

    ('HA103', 'Delhi', 'Bengaluru', '07:30 AM', '10:20 AM', 9499, '2h 50m'),
    ('HA104', 'Bengaluru', 'Delhi', '06:00 PM', '08:50 PM', 9299, '2h 50m'),

    ('HA105', 'Delhi', 'Kolkata', '10:15 AM', '12:30 PM', 8999, '2h 15m'),
    ('HA106', 'Kolkata', 'Delhi', '04:30 PM', '06:50 PM', 8799, '2h 20m'),

    ('HA107', 'Delhi', 'Chennai', '08:45 AM', '11:40 AM', 9999, '2h 55m'),
    ('HA108', 'Chennai', 'Delhi', '05:15 PM', '08:10 PM', 9799, '2h 55m'),

    ('HA109', 'Delhi', 'Hyderabad', '11:30 AM', '01:45 PM', 8499, '2h 15m'),
    ('HA110', 'Hyderabad', 'Delhi', '07:00 PM', '09:20 PM', 8299, '2h 20m'),

    ('HA111', 'Mumbai', 'Bengaluru', '08:20 AM', '09:55 AM', 6999, '1h 35m'),
    ('HA112', 'Bengaluru', 'Mumbai', '03:30 PM', '05:10 PM', 6799, '1h 40m'),

    ('HA113', 'Mumbai', 'Kolkata', '09:45 AM', '12:25 PM', 9499, '2h 40m'),
    ('HA114', 'Kolkata', 'Mumbai', '06:15 PM', '08:55 PM', 9299, '2h 40m'),

    ('HA115', 'Mumbai', 'Chennai', '07:15 AM', '09:10 AM', 7999, '1h 55m'),
    ('HA116', 'Chennai', 'Mumbai', '02:30 PM', '04:30 PM', 7799, '2h 00m'),

    ('HA117', 'Mumbai', 'Hyderabad', '10:30 AM', '12:05 PM', 7499, '1h 35m'),
    ('HA118', 'Hyderabad', 'Mumbai', '04:45 PM', '06:20 PM', 7299, '1h 35m'),

    ('HA119', 'Bengaluru', 'Chennai', '09:00 AM', '10:05 AM', 5499, '1h 05m'),
    ('HA120', 'Chennai', 'Bengaluru', '06:30 PM', '07:35 PM', 5299, '1h 05m'),

    ('HA121', 'Delhi', 'Jaipur', '08:00 AM', '09:00 AM', 4999, '1h 00m'),
    ('HA122', 'Jaipur', 'Delhi', '05:00 PM', '06:05 PM', 4799, '1h 05m'),

    ('HA123', 'Delhi', 'Goa', '06:45 AM', '09:20 AM', 10499, '2h 35m'),
    ('HA124', 'Goa', 'Delhi', '07:30 PM', '10:05 PM', 9999, '2h 35m'),

    ('HA125', 'Mumbai', 'Goa', '11:00 AM', '12:10 PM', 5999, '1h 10m'),
    ('HA126', 'Goa', 'Mumbai', '04:00 PM', '05:15 PM', 5799, '1h 15m'),

    ('HA127', 'Delhi', 'Ahmedabad', '10:00 AM', '11:35 AM', 6499, '1h 35m'),
    ('HA128', 'Ahmedabad', 'Delhi', '06:00 PM', '07:40 PM', 6299, '1h 40m'),

    ('HA129', 'Delhi', 'Pune', '12:00 PM', '02:05 PM', 7999, '2h 05m'),
    ('HA130', 'Pune', 'Delhi', '05:30 PM', '07:40 PM', 7799, '2h 10m'),

    ('HA131', 'Bengaluru', 'Hyderabad', '08:30 AM', '09:35 AM', 5499, '1h 05m'),
    ('HA132', 'Hyderabad', 'Bengaluru', '07:00 PM', '08:10 PM', 5299, '1h 10m'),

    ('HA133', 'Kolkata', 'Bengaluru', '06:45 AM', '09:25 AM', 9499, '2h 40m'),
    ('HA134', 'Bengaluru', 'Kolkata', '05:45 PM', '08:30 PM', 9299, '2h 45m'),

    ('HA135', 'Chennai', 'Kolkata', '09:30 AM', '12:05 PM', 8999, '2h 35m'),
    ('HA136', 'Kolkata', 'Chennai', '06:00 PM', '08:40 PM', 8799, '2h 40m'),

    # ───────────── INTERNATIONAL ─────────────

    ('HA201', 'Delhi', 'Dubai', '01:30 PM', '05:45 PM', 23999, '4h 15m'),
    ('HA202', 'Dubai', 'Delhi', '09:00 PM', '02:00 AM', 22999, '4h 00m'),

    ('HA203', 'Mumbai', 'Dubai', '06:20 PM', '08:15 PM', 21999, '3h 55m'),
    ('HA204', 'Dubai', 'Mumbai', '10:30 PM', '03:00 AM', 20999, '3h 30m'),

    ('HA205', 'Delhi', 'Singapore', '11:15 PM', '07:20 AM', 28999, '5h 05m'),
    ('HA206', 'Singapore', 'Delhi', '09:30 AM', '01:15 PM', 27999, '5h 15m'),

    ('HA207', 'Mumbai', 'Singapore', '10:00 PM', '06:30 AM', 29999, '6h 30m'),
    ('HA208', 'Singapore', 'Mumbai', '08:00 AM', '11:45 AM', 28999, '6h 45m'),

    ('HA209', 'Delhi', 'London', '02:00 AM', '07:00 AM', 52999, '10h 30m'),
    ('HA210', 'London', 'Delhi', '10:00 AM', '11:30 PM', 51999, '9h 30m'),

    ('HA211', 'Mumbai', 'London', '07:45 PM', '05:30 AM', 52999, '10h 45m'),
    ('HA212', 'London', 'Mumbai', '09:30 AM', '10:00 PM', 51999, '9h 30m'),

    ('HA213', 'Delhi', 'Paris', '10:00 PM', '06:45 AM', 47999, '8h 45m'),
    ('HA214', 'Paris', 'Delhi', '10:30 AM', '11:55 PM', 46999, '8h 55m'),

    ('HA215', 'Delhi', 'New York', '09:30 PM', '06:00 AM', 68999, '14h 30m'),
    ('HA216', 'New York', 'Delhi', '11:00 AM', '11:30 AM', 67999, '13h 00m'),

    ('HA217', 'Delhi', 'Tokyo', '08:10 PM', '07:00 AM', 55999, '9h 50m'),
    ('HA218', 'Tokyo', 'Delhi', '10:30 AM', '04:00 PM', 54999, '9h 00m'),

    ('HA219', 'Mumbai', 'Bangkok', '11:30 PM', '07:00 AM', 25999, '4h 00m'),
    ('HA220', 'Bangkok', 'Mumbai', '09:00 AM', '12:30 PM', 24999, '4h 00m'),

    ('HA221', 'Delhi', 'Kathmandu', '09:15 AM', '11:05 AM', 14999, '1h 50m'),
    ('HA222', 'Kathmandu', 'Delhi', '01:00 PM', '02:50 PM', 13999, '1h 50m'),

    ('HA223', 'Mumbai', 'Colombo', '02:30 PM', '05:30 PM', 19999, '3h 00m'),
    ('HA224', 'Colombo', 'Mumbai', '06:30 PM', '09:30 PM', 18999, '3h 00m'),

    ('HA225', 'Delhi', 'Istanbul', '06:00 PM', '10:15 PM', 42999, '7h 45m'),
    ('HA226', 'Istanbul', 'Delhi', '11:30 PM', '07:30 AM', 41999, '6h 30m'),

    ('HA227', 'Delhi', 'Doha', '04:30 PM', '06:45 PM', 24999, '4h 15m'),
    ('HA228', 'Doha', 'Delhi', '09:00 PM', '03:00 AM', 23999, '4h 00m'),

    ('HA229', 'Mumbai', 'Abu Dhabi', '08:30 PM', '10:45 PM', 22999, '3h 45m'),
    ('HA230', 'Abu Dhabi', 'Mumbai', '02:00 AM', '07:00 AM', 21999, '3h 30m'),
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
