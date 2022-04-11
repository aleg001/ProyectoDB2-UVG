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
import psycopg2.extras


"""
Referencia para Flask + React:
https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9
"""
# API para React
from flask_restful import *

# from api.HelloApiHandler import HelloApiHandler

# regex
import re

# hash
from werkzeug.security import *

# coneccion a base de datos con psycopg2 a elephantsql

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
# cursor.execute("DROP TABLE prueba;")


app = Flask(__name__)
# app = Flask(__name__, static_folder="frontend/build")
app.secret_key = "Alecraft_01"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True


# Regular expression operations verify
"""
Referencia:
Documentación oficial de Python3 - https://docs.python.org/3/library/re.html

Correo: r'[^@]+@[^@]+\.[^@]+'

"""

# Encriptacion de contraseña:

"""

Requisito:

12. Las contraseñas de las cuentas deben pasarse por un algoritmo de Hash, como MD5 o
SHA256, y el hash se debe almacenar en la base de datos (no se deben guardar
contraseñas en texto plano)


Referencia: https://www.youtube.com/watch?v=jJ4awOToB6k&ab_channel=PrettyPrinted

Para encriptar con sha256:
generate_password_hash(contraseña, method='sha256')

Para verificar:
check_password_hash(contraseñaEncriptada, contraseña)

"""

# Homepage
@app.route("/")
def index():
    print("xd")


# Logout
@app.route("/logout")
def logout():
    print("xd")


# Login de admin
@app.route("/loginAdmin")
def loginAcmon():
    print("xd")


# Logout de admin
@app.route("/logoutAdmin")
def logoutAcmon():
    print("xd")

# Catalogo
@app.route("/cat")
def cat():
    return render_template("catalogue.html")
    
# Perfil
@app.route("/profile")
def profile():
    print("xd")
    return render_template("profileSelector.html")


# Perfil de admin
@app.route("/adminProfile")
def acmonProfile():
    print("xd")


# Crear cuenta
@app.route("/signup", methods=["POST", "GET"])
def signup():
    print("xd")
    return render_template("signupHHTV.html")


# Login normal
@app.route("/login", methods=["GET", "POST"])
# Login para cuentas registradas en base de datos
def login():

    cur = conn.cursor(cursor_factory=bd.extras.DictCursor)

    if request.method == "POST":
        if "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            selectInfo = "QUERY PENDIENTE"
            cur.execute(selectInfo)
            fetchData = cur.fetchall()

    # flash("Login exitoso!")

    # Se renderiza el login normal
    return render_template("login.html")


# Referencia: https://codeforgeek.com/render-html-file-in-flask/
if __name__ == "__main__":
    app.run(debug=True)
