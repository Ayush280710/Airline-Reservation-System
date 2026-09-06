import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "horizon_airlines_secret_key"

DATABASE = 'airline.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return {
            "id": 1,
            "name": session.get("user_name", "Passenger"),
            "username": session.get("username", "passenger"),
            "email": session.get("user_email", "passenger@example.com")
        }
    
    try:
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        if user:
            return dict(user)
    except Exception as e:
        print("DB Error:", e)
        
    return {
        "id": user_id,
        "name": session.get("user_name", "Passenger"),
        "username": session.get("username", "passenger"),
        "email": session.get("user_email", "passenger@example.com")
    }



@app.route("/")
def home():
    user = get_current_user()
    return render_template("index.html", user=user, current_user=user)


@app.route("/flights", methods=["GET", "POST"])
def flights():
    user = get_current_user()
    return render_template("flights.html", user=user, current_user=user)


@app.route("/booking", methods=["GET", "POST"])
def booking():
    user = get_current_user()
    if request.method == "POST":
        session["pending_flight_name"] = request.form.get("flight_name", "Horizon Sky-402")
        session["pending_source"] = request.form.get("source", "Delhi")
        session["pending_destination"] = request.form.get("destination", "Mumbai")
        session["pending_seats"] = request.form.get("seats", "12A, 12B")
        session["pending_amount"] = request.form.get("amount", "4,500")
        session["pending_passengers"] = request.form.get("passengers", 2)
        
        return redirect(url_for("payment"))
    return render_template("booking.html", user=user, current_user=user)


@app.route("/search", methods=["GET", "POST"])
def search():
    return redirect(url_for("flights"))


@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    user_bookings = session.get("user_bookings", [])
    
    total_bookings_count = len(user_bookings)
    
    total_spent = 0
    for b in user_bookings:
        amount_str = str(b.get("total_amount", "0")).replace(",", "").replace("₹", "").strip()
        try:
            total_spent += float(amount_str)
        except ValueError:
            pass

    return render_template(
        "dashboard.html", 
        user=user, 
        current_user=user, 
        bookings=user_bookings,
        total_bookings=total_bookings_count,
        total_spent=f"{total_spent:,.2f}"
    )

@app.route("/profile")
def profile():
    user_data = get_current_user()
    user_bookings = session.get("user_bookings", [])
    
    return render_template(
        "profile.html", 
        user=user_data, 
        current_user=user_data, 
        bookings=user_bookings
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user_id"] = 1
        session["user_name"] = request.form.get("username", "Passenger")
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/payment", methods=["GET", "POST"])
def payment():
    user = get_current_user()
    if request.method == "POST":
        new_booking = {
            "id": f"HZ-{session.get('pending_amount', '98234')}",
            "flight_name": session.get("pending_flight_name", "Horizon Sky-402"),
            "source": session.get("pending_source", "Delhi"),
            "destination": session.get("pending_destination", "Mumbai"),
            "seats": session.get("pending_seats", "12A, 12B"),
            "total_amount": session.get("pending_amount", "4,500"),
            "passengers_count": session.get("pending_passengers", 2)
        }
        
        bookings = session.get("user_bookings", [])
        bookings.append(new_booking)
        session["user_bookings"] = bookings
        session["last_booking"] = new_booking

        return redirect(url_for("receipt"))

    pending_data = {
        "total_amount": session.get("pending_amount", "4,500"),
        "passengers_count": session.get("pending_passengers", 2),
        "seats_str": session.get("pending_seats", "12A, 12B")
    }
    return render_template("payment.html", pending=pending_data, user=user, current_user=user)

@app.route("/receipt")
def receipt():
    user = get_current_user()
    booking = session.get("last_booking", {})
    flight = {
        "name": booking.get("flight_name", "Horizon Sky-402"),
        "source": booking.get("source", "Delhi"),
        "destination": booking.get("destination", "Mumbai")
    }
    return render_template("receipt.html", booking=booking, flight=flight, user=user, current_user=user)

@app.route("/ticket")
def ticket():
    user = get_current_user()
    booking = session.get("last_booking", {})
    return render_template("ticket.html", booking=booking, user=user, current_user=user)


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/admin")
def admin():
    return redirect(url_for("admin_login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/<path:invalid_route>")
def fallback_route(invalid_route):
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)