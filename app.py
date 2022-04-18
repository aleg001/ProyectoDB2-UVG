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
from datetime import datetime

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

# Creacion aleatoria de ID para usuario
def IDUsuario():
    randomID = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(50)]
    )
    return randomID


def IDTrailerRandom():
    randomID = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(80)]
    )
    return randomID


def IDAnuncioRandom():
    randomID = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(100)]
    )
    return randomID


def IDIntentoFallido():
    randomID = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(30)]
    )
    return randomID


# Fecha de creacion de cuenta
def CreationDate():
    valorRaw = time.time()
    timeObj = time.localtime(valorRaw)
    stringUnificado = "{0}-{1}-{2} {3}:{4}:{5}".format(
        timeObj.tm_mon,
        timeObj.tm_mday,
        timeObj.tm_year,
        timeObj.tm_hour,
        timeObj.tm_min,
        timeObj.tm_sec,
    )
    return stringUnificado


def FechaActual():
    valorRaw = time.time()
    timeObj = time.localtime(valorRaw)
    stringUnificado = "{0}-{1}-{2} {3}:{4}:{5}".format(
        timeObj.tm_mon,
        timeObj.tm_mday,
        timeObj.tm_year,
        timeObj.tm_hour,
        timeObj.tm_min,
        timeObj.tm_sec,
    )
    return stringUnificado


# Variable global
contadorIntentosFallidos = 0


@app.route("/horasPico")
def horasPico():
    return render_template("horasPicos.html")


@app.route("/estadisticaHorasPico", methods=["POST"])
def estadisticaHorasPico():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        date = request.form["date"]

        cur.execute(
            """
        SELECT tiempo FROM(
        SELECT DISTINCT r.fecha_rep::time AS tiempo, count(*) as Conteo
        FROM reproduccion r 
        WHERE r.fecha_rep::date BETWEEN  (SELECT TO_DATE('{0}', 'YYYY-MM-DD')) AND  (SELECT TO_DATE('{0}', 'YYYY-MM-DD'))
        GROUP by tiempo
        ORDER BY Conteo DESC 
        LIMIT 1) as xd; """.format(
                date
            )
        )

        HorasPico = cur.fetchall()
        print(HorasPico)
        # [[datetime.time(21, 0)], [datetime.time(20, 0)], [datetime.time(16, 0)]]
        horasPicoValue = str(HorasPico[0])
        horasPicoValue = horasPicoValue.replace("[", "")
        horasPicoValue = horasPicoValue.replace("]", "")
        horasPicoValue = horasPicoValue.replace("(", " ")
        horasPicoValue = horasPicoValue.replace(")", " hrs")
        horasPicoValue = horasPicoValue.replace(",", ":")
        horasPicoValue = horasPicoValue.replace(" ", "")
        horasPicoValue = horasPicoValue.replace("datetime.time", "Hora pico: ")
        print(horasPicoValue)
        flash(horasPicoValue)
        conn.commit()
        cur.close()

        return render_template("horasPicos.html")


@app.route("/cantRepro", methods=["POST"])
def cantRepro():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        date1 = request.form["dateI"]
        date2 = request.form["dateF"]

        cur.execute(
            """
            SELECT COUNT(r.*) AS cant_reps, t.categoria_t, s.tipo 
            FROM reproduccion r
            LEFT JOIN trailer t ON r.id_vid = t.id_trailer
            LEFT JOIN perfil p ON r.id_per = p.id_perfil
            LEFT JOIN suscripcion s ON p.id_usuario = s.id_user
            WHERE r.fecha_rep::date BETWEEN (SELECT TO_DATE('{0}', 'YYYY-MM-DD')) and (SELECT TO_DATE('{1}', 'YYYY-MM-DD')) 
            GROUP BY t.genero_t, t.categoria_t, s.tipo 
            ORDER BY cant_reps DESC;
            """.format(
                date1, date2
            )
        )

        Repros = cur.fetchall()
        strTemp = ""
        strFinal = ""
        """"
        for i in Repros:
            strTemp = str(Repros[i])
            strFinal = strTemp.replace("[", "")
            strFinal = strTemp.replace("]", "")
            strFinal = strTemp.replace("(", " ")
            strFinal = strTemp.replace(")", "")"""

        flash(Repros)
        conn.commit()
        cur.close()
        # cantidadrepro = cur.fetchall()
    return render_template("cantidadRepro.html")


@app.route("/agregarUser", methods=["POST"])
def agregarUser():
    IDActual = IDUsuario()
    RandomID = IDUsuario()
    isNotActive = False
    date = CreationDate()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":

        name = request.form["name"]
        # Sanitacion de inputs
        name = name.replace("'", "")
        name = name.replace("--", "")
        lastname = request.form["lastname"]
        # Sanitacion de inputs
        lastname = lastname.replace("'", "")
        lastname = lastname.replace("--", "")
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        # Sanitacion de inputs
        email = email.replace("'", "")
        email = email.replace("--", "")
        username = request.form["username"]
        # Sanitacion de inputs
        username = username.replace("'", "")
        username = username.replace("--", "")

        password = request.form["pass"]
        password = password.replace("'", "")
        password = password.replace("--", "")
        passHash = generate_password_hash(password, method="sha256")

        dpi = request.form["DPI"]
        # Sanitacion de inputs
        dpi = dpi.replace("'", "")
        dpi = dpi.replace("--", "")
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
            INSERT INTO perfil VALUES ('{0}', '{1}', '{2}', '{3}');
            """.format(
                RandomID, IDActual, username, isNotActive
            )
        )
    # pruebas = cur.fetchall()
    # print(pruebas)

    conn.commit()
    cur.close()
    return redirect(url_for("login"))


# Homepage
@app.route("/")
def index():
    return redirect(url_for("login"))


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


# Agregar un nuevo director
@app.route("/agregarDirector", methods=["POST"])
def agregarDirector():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_director"
    if request.method == "POST":
        name = request.form["name"]
        # Sanitazacion de inputs
        name = name.replace("'", "")
        name = name.replace("--", "")
        lastname = request.form["lastname"]
        # Sanitazacion de inputs
        lastname = lastname.replace("'", "")
        lastname = lastname.replace("--", "")
        dpi = request.form["dpi"]
        # Sanitazacion de inputs
        dpi = dpi.replace("'", "")
        dpi = dpi.replace("--", "")

        cur.execute(
            """
            SELECT * FROM director WHERE id_director = '{0}';
            """.format(
                dpi
            )
        )
        variable = cur.fetchone()

        if variable:
            flash("El director ingresado ya existe")
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
        cur.close()

    return redirect(url_for(return_var))


# Agregar un nuevo actor
@app.route("/agregarActor", methods=["POST"])
def agregarActor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_actor"
    if request.method == "POST":

        name = request.form["name"]
        # Sanitazacion de inputs
        name = name.replace("'", "")
        name = name.replace("--", "")

        lastname = request.form["lastname"]
        # Sanitazacion de inputs
        lastname = lastname.replace("'", "")
        lastname = lastname.replace("--", "")

        dpi = request.form["dpi"]
        # Sanitazacion de inputs
        dpi = dpi.replace("'", "")
        dpi = dpi.replace("--", "")

        cur.execute(
            """
            SELECT * FROM actor WHERE id_actor = '{0}';
            """.format(
                dpi
            )
        )
        variable = cur.fetchone()

        if variable:
            flash("El actor ya existe")
        else:
            # Creacion de nuevo actor
            cur.execute(
                """
                INSERT INTO actor VALUES ('{0}', '{1}', '{2}');
                """.format(
                    dpi, name, lastname
                )
            )
            conn.commit()
            return_var = "cat"
        cur.close()
    return redirect(url_for(return_var))


# Agregar un nuevo anunciante
@app.route("/agregarAnunciante", methods=["POST"])
def agregarAnunciante():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_anunciante"
    if request.method == "POST":
        name = request.form["name"]
        # Sanitazacion de inputs
        name = name.replace("'", "")
        name = name.replace("--", "")

        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM anunciante WHERE id_anunciante = '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            flash("El anunciante ya existe")
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
        cur.close()

    return redirect(url_for(return_var))


@app.route("/agregarAnuncio", methods=["POST"])
def agregarAnuncio():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "add_advertisment"
    anuncioID = IDAnuncioRandom()
    if request.method == "POST":
        id = request.form["id_anun"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")
        url_ad = request.form["url"]
        descri = request.form["desc"]
        # Sanitazacion de inputs
        descri = descri.replace("'", "")
        descri = descri.replace("--", "")

        cur.execute(
            """
            SELECT * FROM anunciante WHERE id_anunciante = '{0}';
            """.format(
                id
            )
        )
        variable2 = cur.fetchone()

        if variable2 != None:
            # Creacion de nuevo director
            cur.execute(
                """
                INSERT INTO anuncio VALUES ('{0}', '{1}', '{2}', '{3}');
                """.format(
                    anuncioID, id, url_ad, descri
                )
            )
            return_var = "cat"

            conn.commit()
        else:
            flash("El anunciante ingresado no existe")
        cur.close()

    return redirect(url_for(return_var))


# Agregar Trailer
@app.route("/agregarTrailer", methods=["POST"])
def agregarTrailer():
    return_var = "add_trailer"
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        IDTrailer = request.form["id"]
        # Sanitazacion de inputs
        IDTrailer = IDTrailer.replace("'", "")
        IDTrailer = IDTrailer.replace("--", "")
        title = request.form["title"]
        # Sanitazacion de inputs
        title = title.replace("'", "")
        title = title.replace("--", "")
        genre = request.form["genre"]
        # Sanitazacion de inputs
        genre = genre.replace("'", "")
        genre = genre.replace("--", "")
        category = request.form["category"]
        # Sanitazacion de inputs
        category = category.replace("'", "")
        category = category.replace("--", "")
        tiempo = request.form["time"]
        # Sanitazacion de inputs
        tiempo = tiempo.replace("'", "")
        tiempo = tiempo.replace("--", "")
        director = request.form["director"]
        # Sanitazacion de inputs
        director = director.replace("'", "")
        director = director.replace("--", "")
        prota = request.form["prota"]
        # Sanitazacion de inputs
        prota = prota.replace("'", "")
        prota = prota.replace("--", "")
        premios = request.form["awards"]
        # Sanitazacion de inputs
        premios = premios.replace("'", "")
        premios = premios.replace("--", "")
        estreno = request.form["date"]
        url = request.form["url"]
        resumen = request.form["summary"]
        # Sanitazacion de inputs
        resumen = resumen.replace("'", "")
        resumen = resumen.replace("--", "")
        anuncio = request.form["ad"]
        anuncio = anuncio.replace("'", "")
        anuncio = anuncio.replace("--", "")

        cur.execute(
            """
            SELECT * FROM trailer WHERE id_trailer = '{0}';
            """.format(
                IDTrailer
            )
        )
        existencia = cur.fetchone()

        if existencia:
            flash("El trailer ya existe")
        else:
            cur.execute(
                """
                SELECT * FROM genero WHERE id_genero = '{0}';
                """.format(
                    genre
                )
            )
            existencia_genero = cur.fetchone()

            if existencia_genero != None:
                cur.execute(
                    """
                    SELECT * FROM categoria WHERE id_categoria = '{0}';
                    """.format(
                        category
                    )
                )
                existencia_category = cur.fetchone()

                if existencia_category != None:
                    cur.execute(
                        """
                        SELECT * FROM director WHERE id_director = '{0}';
                        """.format(
                            director
                        )
                    )
                    existencia_director = cur.fetchone()
                    if existencia_director != None:
                        cur.execute(
                            """
                            SELECT * FROM actor WHERE id_actor = '{0}';
                            """.format(
                                prota
                            )
                        )
                        existencia_prota = cur.fetchone()
                        if existencia_prota != None:
                            cur.execute(
                                """
                                SELECT * FROM anuncio WHERE id_anuncio = '{0}';
                                """.format(
                                    anuncio
                                )
                            )
                            existencia_anuncio = cur.fetchone()
                            if existencia_anuncio != None:
                                cur.execute(
                                    """
                                    INSERT INTO trailer VALUES ('{0}', '{1}', '{2}','{3}', '{4}', '{5}','{6}', '{7}', '{8}','{9}', '{10}', '{11}');
                                    """.format(
                                        IDTrailer,
                                        title,
                                        genre,
                                        category,
                                        estreno,
                                        director,
                                        prota,
                                        premios,
                                        url,
                                        resumen,
                                        anuncio,
                                        tiempo,
                                    )
                                )
                                conn.commit()
                                return_var = "cat"
                            else:
                                flash("El anuncio ingresado no existe")
                        else:
                            flash("El actor ingresado no existe")
                    else:
                        flash("El director ingresado no existe")
                else:
                    flash("La categoria ingresada no existe")

            else:
                flash("El genero ingresado no existe")
        cur.close()
    return redirect(url_for(return_var))


# Crear cuenta
@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signupHHTV.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/verificarUser", methods=["POST"])
def verificarUser():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    global contadorIntentosFallidos

    if request.method == "POST":

        email = request.form["username"]
        # Sanitazacion de inputs
        email = email.replace("'", "")
        email = email.replace("--", "")

        password = request.form["psw"]
        # Sanitazacion de inputs
        password = password.replace("'", "")
        password = password.replace("--", "")
        # print(password)
        passHash = generate_password_hash(password, method="sha256")
        # print(email)
        # print(passHash)
        intentoFallido = IDIntentoFallido()
        intentoFecha = FechaActual()

        # print(intentoFallido)
        # print(intentoFecha)

        cur.execute(
            """
            SELECT * FROM usuario WHERE correo LIKE '{0}'
            """.format(
                email
            )
        )

        CorreoExistente = cur.fetchone()

        if CorreoExistente:
            contraHash = CorreoExistente["contrasena"]
            verificarPass = check_password_hash(contraHash, password)
            if verificarPass:
                flash("Creedenciales VALIDOS")
                return redirect(url_for("cat"))
            else:
                contadorIntentosFallidos = contadorIntentosFallidos + 1
                # print("CONTADOR 1: ", contadorIntentosFallidos)
                cur.execute(
                    """ 
                INSERT INTO intentosFallidos VALUES ('{0}', '{1}', '{2}');
                """.format(
                        intentoFallido, email, intentoFecha
                    )
                )
                flash("Contraseña equivocada")
                return redirect(url_for("login"))
        else:
            contadorIntentosFallidos = contadorIntentosFallidos + 1
            # print("CONTADOR 2: ", contadorIntentosFallidos)

            cur.execute(
                """ 
                INSERT INTO intentosFallidos VALUES ('{0}', '{1}', '{2}');
            """.format(
                    intentoFallido, email, intentoFecha
                )
            )
            flash("Correo invalido")
            return redirect(url_for("login"))

    conn.commit()
    cur.close()
    flash("Credenciales invalidos 3")
    # contadorIntentosFallidos = contadorIntentosFallidos + 1
    # print("CONTADOR FINAL: ", contadorIntentosFallidos)
    return redirect(url_for("login"))


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


@app.route("/top10")
def top10():
    return render_template("top10Generos.html")


@app.route("/cantRep")
def cantRep():
    return render_template("cantidadRepro.html")


@app.route("/estadisticaGenero", methods=["POST"])
def estadisticaGenero():
    print("XD")


@app.route("/estadisticaCantidad", methods=["POST"])
def estadisticaCantidad():
    print("XD")


@app.route("/reportes", methods=["GET", "POST"])
def reportes():
    return render_template("reportesAdmin.html")


# Referencia: https://codeforgeek.com/render-html-file-in-flask/
if __name__ == "__main__":
    app.run(debug=True)
