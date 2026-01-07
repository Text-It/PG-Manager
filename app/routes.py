from psycopg2 import OperationalError
import psycopg2
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: implement authentication
        # email = request.form.get('email')
        # password = request.form.get('password')
        return redirect(url_for('main.index'))
    return render_template('login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # TODO: implement user creation and validation
        # name = request.form.get('name')
        # email = request.form.get('email')
        # password = request.form.get('password')
        return redirect(url_for('main.index'))
    return render_template('signup.html')


@bp.route('/owner/dashboard')
def owner_dashboard():
    return render_template('owner/dashboard.html')

DB_CONFIG = {
    "dbname": "pgmanagement",
    "user": "pguser",
    "password": "pgpassword",
    "host": "localhost",
    "port": 5433
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except OperationalError:
        return None


@bp.route("/admin", methods=["GET"])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500

    cur = conn.cursor()
    cur.execute("SELECT t_id, t_name, t_email FROM tenants;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ])


@bp.route("/admin", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tenants (t_name, t_email) VALUES (%s, %s) RETURNING t_id;",
        (data["name"], data["email"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id}), 201