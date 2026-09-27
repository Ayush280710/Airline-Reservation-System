from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db, init_db
from functools import wraps
from datetime import date
import secrets
import string
import re

app = Flask(__name__)
app.secret_key = 'horizon-airlines-school-project-2026'
init_db()

CLASS_MULTIPLIERS = {
    'Economy': 1.0,
    'Business': 1.75,
    'First Class': 2.5,
}
PAYMENT_METHODS = ['UPI', 'Credit/Debit Card', 'Net Banking']


def current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    db.close()
    return user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def make_pnr():
    chars = string.ascii_uppercase + string.digits
    while True:
        pnr = 'HA' + ''.join(secrets.choice(chars) for _ in range(6))
        db = get_db()
        exists = db.execute('SELECT 1 FROM bookings WHERE pnr = ?', (pnr,)).fetchone()
        db.close()
        if not exists:
            return pnr


def valid_flight(flight_id):
    db = get_db()
    flight = db.execute('SELECT * FROM flights WHERE id = ?', (flight_id,)).fetchone()
    db.close()
    return flight


@app.context_processor
def inject_user():
    return {'current_user': current_user()}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or not password:
            flash('Please complete all fields.', 'error')
            return render_template('register.html')

        digit_count = sum(ch.isdigit() for ch in password)
        special_count = sum(not ch.isalnum() for ch in password)
        if len(password) < 8 or digit_count < 3 or special_count < 1 or not any(ch.isupper() for ch in password):
            flash('Password must be at least 8 characters long, contain at least 3 numbers, 1 special character and 1 uppercase letter.', 'error')
            return render_template('register.html')

        db = get_db()
        try:
            db.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            db.commit()
        except Exception:
            db.close()
            flash('An account with that email already exists.', 'error')
            return render_template('register.html')
        db.close()
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    user = current_user()
    db = get_db()
    bookings = db.execute('''
        SELECT b.*, f.flight_no, f.source, f.destination, f.departure, f.arrival
        FROM bookings b JOIN flights f ON b.flight_id = f.id
        WHERE b.user_id = ? ORDER BY b.id DESC
    ''', (user['id'],)).fetchall()
    db.close()
    return render_template('profile.html', user=user, bookings=bookings)


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    db = get_db()
    total = db.execute('SELECT COUNT(*) AS c FROM bookings WHERE user_id = ?', (user['id'],)).fetchone()['c']
    db.close()
    return render_template('dashboard.html', user=user, total_bookings=total)


@app.route('/flights')
def flights():
    source = request.args.get('from', '').strip()
    destination = request.args.get('to', '').strip()
    db = get_db()
    if source and destination:
        rows = db.execute('SELECT * FROM flights WHERE lower(source)=lower(?) AND lower(destination)=lower(?)', (source, destination)).fetchall()
    else:
        rows = db.execute('SELECT * FROM flights ORDER BY id').fetchall()
    db.close()
    return render_template('flights.html', flights=rows, search_from=source, search_to=destination)


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    db = get_db()
    flights = db.execute('SELECT * FROM flights ORDER BY source, destination').fetchall()
    db.close()

    selected_id = request.args.get('flight_id', type=int)
    selected_flight = valid_flight(selected_id) if selected_id else None

    if request.method == 'POST':
        flight_id = request.form.get('flight_id', type=int)
        travel_date = request.form.get('date', '')
        passenger_count = request.form.get('passengers', type=int)
        travel_class = request.form.get('travel_class', 'Economy')
        names = [n.strip() for n in request.form.getlist('passenger_name') if n.strip()]
        flight = valid_flight(flight_id)

        if not flight:
            flash('That flight is not available. Please select a listed flight.', 'error')
            return render_template('booking.html', flights=flights, selected_flight=None, today=date.today().isoformat())
        if travel_date < date.today().isoformat():
            flash('Travel date cannot be in the past.', 'error')
            return render_template('booking.html', flights=flights, selected_flight=flight, today=date.today().isoformat())
        if passenger_count not in range(1, 10):
            flash('Passengers must be between 1 and 9.', 'error')
            return render_template('booking.html', flights=flights, selected_flight=flight, today=date.today().isoformat())
        if len(names) != passenger_count:
            flash('Enter a name for every passenger.', 'error')
            return render_template('booking.html', flights=flights, selected_flight=flight, today=date.today().isoformat())
        if travel_class not in CLASS_MULTIPLIERS:
            flash('Please select a valid travel class.', 'error')
            return render_template('booking.html', flights=flights, selected_flight=flight, today=date.today().isoformat())

        total = round(flight['base_price'] * CLASS_MULTIPLIERS[travel_class] * passenger_count)
        pnr = make_pnr()
        db = get_db()
        cur = db.execute('''
            INSERT INTO bookings (pnr, user_id, flight_id, travel_date, passenger_count, travel_class, total_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (pnr, current_user()['id'], flight['id'], travel_date, passenger_count, travel_class, total))
        booking_id = cur.lastrowid

        for index, name in enumerate(names, start=1):
            seat = f'{index}{"A" if index % 2 else "B"}'
            db.execute('INSERT INTO passengers (booking_id, full_name, seat_no) VALUES (?, ?, ?)', (booking_id, name, seat))
        db.commit()
        db.close()
        return redirect(url_for('payment', booking_id=booking_id))

    return render_template('booking.html', flights=flights, selected_flight=selected_flight, today=date.today().isoformat())


@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    db = get_db()
    booking_row = db.execute("""
        SELECT b.*, f.flight_no, f.source, f.destination, f.departure, f.arrival
        FROM bookings b JOIN flights f ON b.flight_id=f.id
        WHERE b.id=? AND b.user_id=?
    """, (booking_id, current_user()['id'])).fetchone()

    if not booking_row:
        db.close()
        return redirect(url_for('profile'))

    if request.method == 'POST':
        method = request.form.get('payment_method', '')
        if method not in PAYMENT_METHODS:
            db.close(); flash('Choose a valid payment method.', 'error')
            return render_template('payment.html', booking=booking_row, methods=PAYMENT_METHODS)

        existing_payment = db.execute('SELECT * FROM payments WHERE booking_id = ?', (booking_id,)).fetchone()
        if existing_payment:
            db.close()
            return redirect(url_for('ticket', booking_id=booking_id))

        transaction_ref = 'HAP' + secrets.token_hex(5).upper()
        try:
            db.execute("""INSERT INTO payments (booking_id, method, transaction_ref, amount)
                         VALUES (?, ?, ?, ?)""", (booking_id, method, transaction_ref, booking_row['total_price']))
            db.execute("""UPDATE bookings SET payment_method=?, payment_status=? WHERE id=?""", (method, 'Paid', booking_id))
            db.commit()
        except Exception:
            db.rollback(); db.close(); raise
        db.close()
        return redirect(url_for('ticket', booking_id=booking_id))

    db.close()
    return render_template('payment.html', booking=booking_row, methods=PAYMENT_METHODS)


@app.route('/ticket/<int:booking_id>')
@login_required
def ticket(booking_id):
    db = get_db()
    booking_row = db.execute('''
        SELECT b.*, f.flight_no, f.source, f.destination, f.departure, f.arrival, f.duration
        FROM bookings b JOIN flights f ON b.flight_id=f.id
        WHERE b.id=? AND b.user_id=?
    ''', (booking_id, current_user()['id'])).fetchone()
    passengers = db.execute('SELECT * FROM passengers WHERE booking_id=? ORDER BY id', (booking_id,)).fetchall()
    payment_row = db.execute('SELECT * FROM payments WHERE booking_id=?', (booking_id,)).fetchone()
    db.close()
    if not booking_row:
        return redirect(url_for('profile'))
    return render_template('ticket.html', booking=booking_row, passengers=passengers, payment=payment_row)


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username', '').strip() == 'admin' and request.form.get('password', '').strip() == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials.', 'error')
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    db = get_db()
    users = db.execute('SELECT * FROM users ORDER BY id DESC').fetchall()
    bookings = db.execute('''
        SELECT b.*, u.name, u.email, f.flight_no, f.source, f.destination
        FROM bookings b JOIN users u ON b.user_id=u.id JOIN flights f ON b.flight_id=f.id
        ORDER BY b.id DESC
    ''').fetchall()
    db.close()
    return render_template('admin_dashboard.html', users=users, bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
