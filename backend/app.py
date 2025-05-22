from flask import Flask, request, jsonify
from flask_cors import CORS
import mariadb
import jwt, datetime, os, time, logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# ── configuration ────────────────────────────────────────────────────────────────
db_cfg = dict(
    host=os.getenv("DB_HOST", "host.containers.internal"),
    user=os.getenv("DB_USER", "appuser"),
    password=os.getenv("DB_PASS", "apppassword"),
    database=os.getenv("DB_NAME", "appdb"),
    port=int(os.getenv("DB_PORT", 3306)),
)
SECRET   = os.getenv("JWT_SECRET", "change-me")
API_ADDR = os.getenv("API_ADDR", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# ── helpers ──────────────────────────────────────────────────────────────────────

def db(retries: int = 15, delay: int = 3):
    """Return a MariaDB connection, retrying a few times if the DB is still coming up."""
    last_exc = None
    for _ in range(retries):
        try:
            return mariadb.connect(**db_cfg)
        except mariadb.Error as exc:
            last_exc = exc
            time.sleep(delay)
    raise last_exc


def init_db():
    """Ensure the required tables exist."""
    ddl = """
        CREATE TABLE IF NOT EXISTS bulletins (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            title     VARCHAR(255) NOT NULL,
            price     DECIMAL(10,2) NOT NULL,
            location  VARCHAR(255) NOT NULL,
            created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()
    logging.info("Database schema verified / created")

# ── routes ───────────────────────────────────────────────────────────────────────

@app.post("/login")
def login():
    creds = request.get_json(force=True)
    u, p = creds.get("user"), creds.get("pass")
    if u == "admin" and p == "admin":
        token = jwt.encode(
            {"u": u, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)},
            SECRET,
            algorithm="HS256",
        )
        return {"token": token}
    return {"error": "unauthorized"}, 401


@app.get("/bulletins")
def bulletins():
    cur = db().cursor(dictionary=True)
    cur.execute("SELECT id, title, price, location FROM bulletins ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)


@app.post("/bulletins")
def add_bulletin():
    hdr = request.headers.get("Authorization", "")
    try:
        jwt.decode(hdr.split()[1], SECRET, algorithms=["HS256"])
    except Exception:
        return {"error": "unauthorized"}, 401

    data = request.get_json(force=True)
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bulletins(title, price, location) VALUES (%s,%s,%s)",
        (data["title"], data["price"], data["location"]),
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "ok"}


@app.get("/healthcheck")
def healthcheck():
    try:
        cur = db().cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        return {"status": "ok"}, 200
    except mariadb.Error as e:
        logging.exception("DB healthcheck failed")
        return {
            "status": "db_error",
            "errno": e.errno,
            "msg": e.msg,
            "host": db_cfg["host"],
            "port": db_cfg["port"],
        }, 500

# ── entrypoint ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(host=API_ADDR, port=API_PORT)
