from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")



@app.route("/flights")
def flights():
    return render_template("flights.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/ticket")
def ticket():
    return render_template("ticket.html")


@app.route("/admin/login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)