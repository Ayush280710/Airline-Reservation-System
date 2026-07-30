from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        print("Email:", email)
        print("Password:", password)

        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        print("Name:", name)
        print("Email:", email)
        print("Password:", password)

        return redirect(url_for("login"))

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

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Simple admin credentials
        if username == "admin" and password == "admin123":
            return redirect(url_for("admin_dashboard"))

        return "Invalid Admin Credentials"

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)