""""
Proyecto #2 de Base de Datos
Universidad del Valle de Guatemala 2022
Bases de Datos 1 sección 11


Alejandro Gómez - 20347
Marco Jurado - 20308
Cristian Aguirre - 20231
"""

# imports
from flask import *
import os
import urllib.parse as up
import psycopg2 as bd

# coneccion a base de datos con psycopg2 a elephantsql
"""
up.uses_netloc.append("postgres")
url = up.urlparse(
    os.environ[
        "postgres://zxzqzikf:BspqkwRodadqDN_71iCKb2Go16puePOD@heffalump.db.elephantsql.com/zxzqzikf"
    ]
)
conn = bd.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
)
"""
conn = bd.connect(
    database="zxzqzikf",
    user="zxzqzikf",
    password="BspqkwRodadqDN_71iCKb2Go16puePOD",
    host="heffalump.db.elephantsql.com",
    port=5432,
)

conn.autocommit = (
    True  # Ensure data is added to the database immediately after write commands
)
cursor = conn.cursor()
cursor.execute("INSERT INTO prueba VALUES (420, 'CristianBro');")


app = Flask(__name__)


@app.route("/Login", methods=["POST", "GET"])
def index():

    cur = conn.cursor(cursor_factory=bd.extras.DictCursor)

    cur.execute(
        """
        INSERT INTO prueba VALUES (420, 'CristianBro');
        """,
    )
    conn.commit()
    flash("Tabla borrada")

    return "<h1> HHTV </h1>"
