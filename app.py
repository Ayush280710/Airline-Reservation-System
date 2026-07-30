from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = []
bookings = []

logged_in_user = None


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        user = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        }

        users.append(user)

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    global logged_in_user

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        for user in users:

            if user["email"] == email and user["password"] == password:

                logged_in_user = user

                return redirect(url_for("profile"))

        return "<h2>Invalid Email or Password</h2>"

    return render_template("login.html")


@app.route("/logout")
def logout():

    global logged_in_user

    logged_in_user = None

    return redirect(url_for("home"))


@app.route("/profile")
def profile():

    if logged_in_user is None:
        return redirect(url_for("login"))

    user_bookings = []

    for booking in bookings:

        if booking["email"] == logged_in_user["email"]:
            user_bookings.append(booking)

    return render_template(
        "profile.html",
        user=logged_in_user,
        bookings=user_bookings
    )


@app.route("/dashboard")
def dashboard():

    if logged_in_user is None:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user=logged_in_user,
        total_bookings=len(bookings)
    )

@app.route("/flights")
def flights():
    return render_template("flights.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():

    if logged_in_user is None:
        return redirect(url_for("login"))

    if request.method == "POST":

        booking = {

            "name": logged_in_user["name"],

            "email": logged_in_user["email"],

            "source": request.form["source"],

            "destination": request.form["destination"],

            "date": request.form["date"],

            "passengers": request.form["passengers"]

        }

        bookings.append(booking)

        return redirect(url_for("ticket"))

    return render_template("booking.html")


@app.route("/ticket")
def ticket():

    if len(bookings) == 0:
        return redirect(url_for("booking"))

    latest_booking = bookings[-1]

    return render_template(
        "ticket.html",
        booking=latest_booking
    )

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        print(f"Username='{username}'")
        print(f"Password='{password}'")

        if username.strip() == "admin" and password.strip() == "admin123":
            return redirect(url_for("admin_dashboard"))

        return "Invalid Admin Credentials"

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    return render_template(
        "admin_dashboard.html",
        users=users,
        bookings=bookings
    )

if __name__ == "__main__":
    app.run(debug=True)