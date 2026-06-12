import os
import psycopg2

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():

    try:
        conn = get_connection()
        conn.close()
        estado = "Conectado"
    except:
        estado = "Error de conexión"

    return render_template(
        "index.html",
        app_name=APP_NAME,
        version=APP_VERSION,
        estado=estado
    )


@app.route("/productos")
def productos():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM productos")

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)