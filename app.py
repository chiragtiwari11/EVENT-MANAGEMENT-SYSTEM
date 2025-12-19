from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_db_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        location TEXT,
        description TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER,
        UNIQUE(user_id, event_id)
    )
    """)

    conn.commit()
    conn.close()


# ---------------- CREATE ADMIN ----------------
def create_admin():
    conn = get_db_connection()
    conn.execute("""
    INSERT OR IGNORE INTO users (id, name, email, password, role)
    VALUES (1, 'Admin', 'admin@gmail.com', 'admin123', 'admin')
    """)
    conn.commit()
    conn.close()


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, "user")
        )
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if session["role"] == "admin":
        return render_template("admin_dashboard.html")
    else:
        return render_template("user_dashboard.html")


@app.route("/add-event", methods=["GET", "POST"])
def add_event():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        location = request.form["location"]
        description = request.form["description"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO events (title, date, location, description) VALUES (?, ?, ?, ?)",
            (title, date, location, description)
        )
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_event.html")


@app.route("/view-events")
def view_events():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()

    return render_template("view_events.html", events=events)



@app.route("/registrations")
def registrations():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db_connection()
    data = conn.execute("""
    SELECT users.name, users.email, events.title
    FROM registrations
    JOIN users ON registrations.user_id = users.id
    JOIN events ON registrations.event_id = events.id
    """).fetchall()
    conn.close()

    return render_template("registrations.html", data=data)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")



if __name__ == "__main__":
    create_tables()
    create_admin()
    app.run(debug=True)

