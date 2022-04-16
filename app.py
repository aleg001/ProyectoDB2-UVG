""""
Proyecto #2 de Base de Datos
Universidad del Valle de Guatemala 2022
Bases de Datos 1 sección 11


Alejandro Gómez - 20347
Marco Jurado - 20308
Cristian Aguirre - 20231
"""

# imports
from urllib import request
from flask import *
from flask import flash
import os
import urllib.parse as up
import psycopg2 as bd
import psycopg2.extras
import random
import string
import time


# Creacion aleatoria de ID para usuario
def IDUsuario():
    randomID = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(50)]
    )
    return randomID


# Fecha de creacion de cuenta
def CreationDate():
    valorRaw = time.time()
    timeObj = time.localtime(valorRaw)
    stringUnificado = "{0}-{1}-{2} {3}:{4}:{5}".format(
        timeObj.tm_mday,
        timeObj.tm_mon,
        timeObj.tm_year,
        timeObj.tm_hour,
        timeObj.tm_min,
        timeObj.tm_sec,
    )
    return stringUnificado


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


# Perfil
@app.route("/agregaPerfil", methods=["POST"])
def profile(idPerfil):
    print("xd")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        name = request.form[""]
    return render_template("p-rofileSelector.html")


# Perfil de admin
@app.route("/adminProfile")
def acmonProfile():
    print("xd")


@app.route("/agregarUser", methods=["POST"])
def agregarUser():
    IDActual = IDUsuario()
    isNotActive = False
    date = CreationDate()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":

        name = request.form["name"]
        lastname = request.form["lastname"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["pass"]
        passHash = generate_password_hash(password, method="sha256")
        dpi = request.form["DPI"]
        isAdmin = request.form["isAdmin"]

        # Creacion de cuenta
        cur.execute(
            """
            INSERT INTO usuario VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');
            """.format(
                IDActual, isAdmin, passHash, date, dpi, name, lastname, email
            )
        )
        # Creacion de primer perfil
        cur.execute(
            """
            INSERT INTO perfil VALUES ('{0}', '{1}', '{2}');
            """.format(
                IDActual, username, isNotActive
            )
        )
    # pruebas = cur.fetchall()
    # print(pruebas)

    conn.commit()
    cur.close()
    return redirect(url_for("login"))

#Agregar un nuevo director
@app.route("/agregarDirector", methods=["POST"])
def agregarDirector():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_director"
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        dpi = request.form["dpi"]

        cur.execute(
            """
            SELECT * FROM director WHERE id_director = '{0}';
            """.format(dpi)
        )
        variable = cur.fetchone()
        
        if variable:
            flash('El director ya existe')
        else:
            # Creacion de nuevo director
            cur.execute(
                """
                INSERT INTO director VALUES ('{0}', '{1}', '{2}');
                """.format(
                    dpi, name, lastname
                )
            )
            return_var = "cat"
            conn.commit()
            flash('El director se ha registrado correctamente')
        cur.close()

    return redirect(url_for(return_var))

#Agregar un nuevo actor
@app.route("/agregarActor", methods=["POST"])
def agregarActor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":

        name = request.form["name"]
        lastname = request.form["lastname"]
        dpi = request.form["dpi"]

        # Creacion de nuevo director
        cur.execute(
            """
            INSERT INTO actor VALUES ('{0}', '{1}', '{2}');
            """.format(
                dpi, name, lastname
            )
        )

    conn.commit()
    cur.close()
    return redirect(url_for("cat"))

#Agregar un nuevo anunciante
@app.route("/agregarAnunciante", methods=["POST"])
def agregarAnunciante():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_anunciante"
    if request.method == "POST":
        name = request.form["name"]
        id = request.form["id"]

        cur.execute(
            """
            SELECT * FROM anunciante WHERE id_anunciante = '{0}';
            """.format(id)
        )
        variable = cur.fetchone()
        
        if variable:
            flash('El anunciante ingresado ya existe')
        else:
            # Creacion de nuevo director
            cur.execute(
                """
                INSERT INTO anunciante VALUES ('{0}', '{1}');
                """.format(
                    id, name
                )
            )
            return_var = "cat"
            conn.commit()
            flash('El anunciante se ha registrado correctamente')
        cur.close()

    return redirect(url_for(return_var))

@app.route("/agregarAnuncio", methods=["POST"])
def agregarAnuncio():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_advertisment"
    if request.method == "POST":
        id_anun = request.form["id_anun"]
        id = request.form["id"]
        url_ad = request.form["url"]
        descri = request.form["desc"]
        cur.execute(
            """
            SELECT * FROM anuncio WHERE id_anuncio = '{0}';
            """.format(id)
        )
        variable = cur.fetchone()

        cur.execute(
            """
            SELECT * FROM anunciante WHERE id_anunciante = '{0}';
            """.format(id_anun)
        )
        variable2 = cur.fetchone()
        
        if variable:
            flash('El anuncio ingresado ya existe')
        else:
            # Creacion de nuevo director
            cur.execute(
                """
                INSERT INTO anuncio VALUES ('{0}', '{1}', '{2}', '{3}');
                """.format(
                    id, id_anun, url_ad, descri 
                )
            )
            return_var = "cat"
            conn.commit()
            flash('El anuncio se ha registrado correctamente')
        cur.close()

    return redirect(url_for(return_var))

# Agregar Trailer
@app.route("/agregarTrailer", methods=["POST"])
def agregarTrailer():
    IDTrailer = IDUsuario()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":

        name = request.form["name"]
        lastname = request.form["lastname"]
        dpi = request.form["dpi"]

        # Creacion de nuevo director
        cur.execute(
            """
            INSERT INTO actor VALUES ('{0}', '{1}', '{2}');
            """.format(
                dpi, name, lastname
            )
        )

    conn.commit()
    cur.close()
    return redirect(url_for("cat"))

# Crear cuenta
@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signupHHTV.html")


# Login normal
@app.route("/login", methods=["GET", "POST"])
# Login para cuentas registradas en base de datos
def login():

    cur = conn.cursor(cursor_factory=bd.extras.DictCursor)

    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        if "username" in request.form and "password" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            passHash = generate_password_hash(password, method="sha256")

            cur.execute(
                """
                SELECT * FROM usuario WHERE username = '{0}' and password = '{1}'
                """.format(
                    username, passHash
                )
            )
            conn.commit()
            cur.close()

            dataExiste = cur.fetchone()

            if dataExiste:
                print(dataExiste)
            else:
                flash("no existe chavo xd")

    # flash("Login exitoso!")

    # Se renderiza el login normal
    return render_template("login.html")


# Catalogo
@app.route("/cat")
def cat():
    return render_template("catalogue.html")

# Busqueda
@app.route("/search")
def search():
    return render_template("search.html")

# Agregar anunciante
@app.route("/addanu")
def add_anunciante():
    return render_template("addAnu.html")

# Agregar director
@app.route("/adddir")
def add_director():
    return render_template("addDir.html")

# Agregar anuncio
@app.route("/addad")
def add_advertisment():
    return render_template("addAd.html")

# Agregar actor
@app.route("/addactor")
def add_actor():
    return render_template("addAct.html")

# Agregar trailer
@app.route("/addtrailer")
def add_trailer():
    return render_template("addTrailer.html")


# Referencia: https://codeforgeek.com/render-html-file-in-flask/
if __name__ == "__main__":
    app.run(debug=True)
