import os
import time
import psycopg2
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ======================
# CONFIG APP
# ======================
APP_NAME = os.getenv("APP_NAME", "Mi App Flask")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# ======================
# CONFIG DB (CORREGIDO)
# ======================
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ======================
# CONEXIÓN ROBUSTA (DOCKER SAFE)
# ======================
def get_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("✅ Conectado a PostgreSQL")
            return conn

        except Exception as e:
            print(f"⏳ Intento {i+1} falló: {e}")
            time.sleep(3)

    raise Exception("❌ No se pudo conectar a PostgreSQL")


# ======================
# HOME
# ======================
@app.route("/")
def home():
    try:
        conn = get_connection()
        conn.close()
        estado = "Conectado a PostgreSQL ✅"
    except Exception as e:
        print("ERROR DB:", e)
        estado = "Error de conexión ❌"

    return render_template(
        "index.html",
        app_name=APP_NAME,
        version=APP_VERSION,
        estado=estado
    )


# ======================
# PRODUCTOS
# ======================
@app.route("/productos")
def productos():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM productos")
        productos = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        print("ERROR CONSULTA:", e)
        productos = []

    return render_template(
        "productos.html",
        productos=productos
    )


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)