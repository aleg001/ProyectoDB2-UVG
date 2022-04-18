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
from flask import flash, session
import os
import urllib.parse as up
import psycopg2 as bd
import psycopg2.extras
import random
import string
import time
from datetime import datetime

from pyrsistent import v

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


# Impresion de Queries


def ImpresionActores(primerAct):
    primerAct = primerAct.replace("[", "")
    primerAct = primerAct.replace("]", "")
    primerAct = primerAct.replace("(", "")
    primerAct = primerAct.replace(")", "")
    primerAct = primerAct.replace(",", "")
    primerAct = "Actor y cantidad películas:", primerAct
    flash(primerAct)
    return primerAct


def ImpresionGenero(genero):
    genero = genero.replace("[", "")
    genero = genero.replace("]", "")
    genero = genero.replace("(", "")
    genero = genero.replace(")", "")
    genero = genero.replace(",", "")
    genero = "Genero y tiempo:", genero
    flash(genero)
    return genero


# Cant_Reproducciones, Categoria y tipo Cuenta


def ImpresionRepro(repro):
    repro = repro.replace("[", "")
    repro = repro.replace("]", "")
    repro = repro.replace("(", "")
    repro = repro.replace(")", "")
    repro = repro.replace(",", "")
    repro = "Reproducciones, categoria y tipo de cuenta:", repro
    flash(repro)
    return repro


# Variable global
contadorIntentosFallidos = 0


@app.route("/horasPico")
def horasPico():
    return render_template("horasPicos.html")


# estadisticas
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
        # Cant_Reproducciones, Categoria y tipo Cuenta
        primerAct = str(Repros[0])
        segundoAct = str(Repros[1])
        tercerAct = str(Repros[2])
        cuartoAct = str(Repros[3])
        QuintoAct = str(Repros[4])
        SextoAct = str(Repros[5])

        ImpresionRepro(primerAct)
        ImpresionRepro(segundoAct)
        ImpresionRepro(tercerAct)
        ImpresionRepro(cuartoAct)
        ImpresionRepro(QuintoAct)
        ImpresionRepro(SextoAct)

        # flash(Repros)
        conn.commit()
        cur.close()
        # cantidadrepro = cur.fetchall()
    return render_template("cantidadRepro.html")


@app.route("/actoresDir", methods=["POST"])
def actoresDir():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cur.execute(
            """
        SELECT a.nombre , COUNT(t.actorprincipal) AS aparicion_actor 
        FROM trailer t 
        LEFT JOIN actor a ON t.actorprincipal = a.id_actor 
        WHERE t.id_trailer IN(
            SELECT r.id_vid 
            FROM reproduccion r
            LEFT JOIN perfil p ON r.id_per = p.id_perfil 
            LEFT JOIN suscripcion s ON p.id_usuario = s.id_user 
            WHERE s.tipo LIKE 'Premium' OR s.tipo LIKE 'Basic'
        )
        GROUP BY a.nombre
        ORDER BY aparicion_actor DESC 
        LIMIT 10;         
        """.format()
        )
        actoresdirectores = cur.fetchall()

        # [[datetime.time(21, 0)], [datetime.time(20, 0)], [datetime.time(16, 0)]]
        primerAct = str(actoresdirectores[0])
        segundoAct = str(actoresdirectores[1])
        tercerAct = str(actoresdirectores[2])
        cuartoAct = str(actoresdirectores[3])
        QuintoAct = str(actoresdirectores[4])
        SextoAct = str(actoresdirectores[5])
        SepAct = str(actoresdirectores[6])
        OctAct = str(actoresdirectores[7])
        NovAct = str(actoresdirectores[8])
        DecAct = str(actoresdirectores[9])

        ImpresionActores(primerAct)
        ImpresionActores(segundoAct)
        ImpresionActores(tercerAct)
        ImpresionActores(cuartoAct)
        ImpresionActores(QuintoAct)
        ImpresionActores(SextoAct)
        ImpresionActores(SepAct)
        ImpresionActores(OctAct)
        ImpresionActores(NovAct)
        ImpresionActores(DecAct)

        # flash(primerAct)

        conn.commit()
        cur.close()
    return render_template("top10Act.html")


@app.route("/actoresDir2", methods=["POST"])
def actoresDir2():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cur.execute(
            """
        select d.nombre, count(t.director_t) as director_apa 
        from trailer t 
        left join director d on t.director_t = d.id_director 
        where t.id_trailer in(
            select r.id_vid 
            from reproduccion r
            left join perfil p on r.id_per = p.id_perfil 
            left join suscripcion s on p.id_usuario = s.id_user 
            where s.tipo like 'Premium' or s.tipo like 'Basic'
        )
        group by d.nombre 
        order by director_apa desc 
        limit 10;         
        """.format()
        )
        actoresdirectores = cur.fetchall()
        primerAct = str(actoresdirectores[0])
        segundoAct = str(actoresdirectores[1])
        tercerAct = str(actoresdirectores[2])
        cuartoAct = str(actoresdirectores[3])
        QuintoAct = str(actoresdirectores[4])
        SextoAct = str(actoresdirectores[5])
        SepAct = str(actoresdirectores[6])
        OctAct = str(actoresdirectores[7])
        NovAct = str(actoresdirectores[8])
        DecAct = str(actoresdirectores[9])

        ImpresionActores(primerAct)
        ImpresionActores(segundoAct)
        ImpresionActores(tercerAct)
        ImpresionActores(cuartoAct)
        ImpresionActores(QuintoAct)
        ImpresionActores(SextoAct)
        ImpresionActores(SepAct)
        ImpresionActores(OctAct)
        ImpresionActores(NovAct)
        ImpresionActores(DecAct)

        conn.commit()
        cur.close()
    return render_template("top10Act.html")


@app.route("/cuentasAvanzadas", methods=["POST"])
def cuentasAvanzadas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cur.execute(
            """ 
        SELECT COUNT(*) 
        FROM suscripcion s 
        LEFT JOIN usuario u ON u.id = s.id_user
        WHERE s.tipo LIKE 'Premium'
        AND u.fechainscripcion BETWEEN (current_date - interval '6 months') AND current_date;        
        """.format()
        )
        cAvanzadas = cur.fetchall()

        conn.commit()
        primerAct = str(cAvanzadas[0])
        primerAct = primerAct.replace("[", "Cuentas: ")
        primerAct = primerAct.replace("]", "")
        flash(primerAct)

        cur.close()

    return render_template("cantAvanzadas.html")


@app.route("/estadisticaGenero", methods=["POST"])
def estadisticaGenero():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":

        date1 = request.form["dateI"]
        date2 = request.form["dateF"]

        cur.execute(
            """ 
            SELECT g.nombregen , SUM(t.tiempo_rep) AS tiempo_reproduccion
            FROM reproduccion r
            LEFT JOIN trailer t ON r.id_vid = t.id_trailer
            LEFT JOIN genero g ON t.genero_t = g.id_genero 
            WHERE r.fecha_rep BETWEEN (SELECT TO_DATE('{0}', 'YYYY-MM-DD')) AND (SELECT TO_DATE('{1}', 'YYYY-MM-DD'))
            GROUP BY g.nombregen 
            ORDER BY tiempo_reproduccion DESC 
            LIMIT 10;       
            """.format(
                date1, date2
            )
        )
        estGen = cur.fetchall()
        primerAct = str(estGen[0])
        segundoAct = str(estGen[1])
        tercerAct = str(estGen[2])
        cuartoAct = str(estGen[3])
        QuintoAct = str(estGen[4])
        SextoAct = str(estGen[5])
        SepAct = str(estGen[6])
        OctAct = str(estGen[7])
        NovAct = str(estGen[8])
        DecAct = str(estGen[9])

        ImpresionActores(primerAct)
        ImpresionActores(segundoAct)
        ImpresionActores(tercerAct)
        ImpresionActores(cuartoAct)
        ImpresionActores(QuintoAct)
        ImpresionActores(SextoAct)
        ImpresionActores(SepAct)
        ImpresionActores(OctAct)
        ImpresionActores(NovAct)
        ImpresionActores(DecAct)

        conn.commit()
        cur.close()
    return render_template("top10Generos.html")


@app.route("/top10")
def top10():
    return render_template("top10Generos.html")


@app.route("/cantRep")
def cantRep():
    return render_template("cantidadRepro.html")


@app.route("/reportes")
def reportes():
    return render_template("reportesAdmin.html")


@app.route("/cuentasAvan")
def cuentasAvan():
    return render_template("cantAvanzadas.html")


@app.route("/top10Actores")
def top10Actores():
    return render_template("top10Act.html")


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


# Eliminar un usuario
@app.route("/eliminarUsuario", methods=["POST"])
def eliminarUsuario():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "deleteuser"
    if request.method == "POST":
        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM usuario WHERE id like '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            # Eliminacion de anunciante
            cur.execute(
                """
                DELETE FROM usuario WHERE id like ('{0}');
                """.format(
                    id
                )
            )
            return_var = "cat"
            conn.commit()
        else:
            flash("El usuario ingresado no existe")
        cur.close()

    return redirect(url_for(return_var))


# Homepage
@app.route("/")
def index():
    return redirect(url_for("login"))


# Logout
@app.route("/logout")
def logout():
    print("xd")


# Login de admin
@app.route("/adminLog", methods=["POST"])
def adminLog():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
            SELECT * FROM usuario WHERE correo LIKE '{0}' and isadmin like 'True'
            """.format(
                email
            )
        )

        CorreoExistente = cur.fetchone()

        if CorreoExistente:
            contraHash = CorreoExistente["contrasena"]
            verificarPass = check_password_hash(contraHash, password)
            if verificarPass:
                cur.execute(
                    """
                    SELECT id_perfil FROM perfil p
                    LEFT JOIN usuario u ON p.id_usuario = u.id
                    WHERE u.correo LIKE '{0}'
                    """.format(
                        email
                    )
                )
                idactual = cur.fetchone()
                session["idactualperfil"] = idactual
                return redirect(url_for("menuadmin"))
            else:
                # contadorIntentosFallidos = contadorIntentosFallidos + 1
                # print("CONTADOR 1: ", contadorIntentosFallidos)
                cur.execute(
                    """ 
                INSERT INTO intentosFallidos VALUES ('{0}', '{1}', '{2}');
                """.format(
                        intentoFallido, email, intentoFecha
                    )
                )
                flash("Contraseña equivocada")
                return redirect(url_for("loginAdmin"))
        else:
            # contadorIntentosFallidos = contadorIntentosFallidos + 1
            # print("CONTADOR 2: ", contadorIntentosFallidos)

            cur.execute(
                """ 
                INSERT INTO intentosFallidos VALUES ('{0}', '{1}', '{2}');
            """.format(
                    intentoFallido, email, intentoFecha
                )
            )
            flash("Correo invalido")
            return redirect(url_for("loginAdmin"))

    conn.commit()
    cur.close()
    flash("Credenciales invalidos 3")
    # contadorIntentosFallidos = contadorIntentosFallidos + 1
    # print("CONTADOR FINAL: ", contadorIntentosFallidos)
    return redirect(url_for("loginAdmin"))


# Login de admin
@app.route("/loginAdmin")
def loginAdmin():
    return render_template("loginAdmin.html")


# menu de admin
@app.route("/menuadmin")
def menuadmin():
    return render_template("menuAdmin.html")


# manejar de anuncios
@app.route("/manAnu")
def manAnu():
    return render_template("manejarAnuncios.html")


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
            return_var = "menuadmin"
            conn.commit()
        cur.close()

    return redirect(url_for(return_var))


# Eliminar un  director
@app.route("/eliminarDirector", methods=["POST"])
def eliminarDirector():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "deletedir"
    if request.method == "POST":
        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM director WHERE id_director = '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            # Eliminacion de director
            cur.execute(
                """
                DELETE FROM director WHERE id_director like '{0}';
                """.format(
                    id
                )
            )
            return_var = "menuadmin"
            conn.commit()
        else:
            flash("El director ingresado no existe")
        cur.close()

    return redirect(url_for(return_var))


# Modificar un director
@app.route("/modDirector", methods=["POST"])
def modDirector():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "moddirector"
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
            # Creacion de nuevo actor
            cur.execute(
                """
                UPDATE director
                 SET id_director ='{0}',
                    nombre='{1}',
                    apellido='{2}'
                 WHERE id_director like '{3}';
                """.format(
                    dpi, name, lastname, dpi
                )
            )
            conn.commit()
            return_var = "menuadmin"
        else:
            flash("El director no existe")
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
            return_var = "menuadmin"
        cur.close()
    return redirect(url_for(return_var))


# Modificar un actor
@app.route("/modActor", methods=["POST"])
def modActor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "modact"
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
            # Creacion de nuevo actor
            cur.execute(
                """
                UPDATE actor
                 SET id_actor='{0}',
                    nombre='{1}',
                    apellido='{2}'
                 WHERE id_actor like '{3}';
                """.format(
                    dpi, name, lastname, dpi
                )
            )
            conn.commit()
            return_var = "menuadmin"
        else:
            flash("El actor no existe")
        cur.close()
    return redirect(url_for(return_var))


# Eliminar un  actor
@app.route("/eliminarActor", methods=["POST"])
def eliminarActor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "deletetrailer"
    if request.method == "POST":
        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM actor WHERE id_actor like '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            # Eliminacion de director
            cur.execute(
                """
                DELETE FROM actor WHERE id_actor like ('{0}');
                """.format(
                    id
                )
            )
            return_var = "menuadmin"
            conn.commit()
        else:
            flash("El actor ingresado no existe")
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
            return_var = "menuadmin"
            conn.commit()
        cur.close()

    return redirect(url_for(return_var))


# Eliminar un  anunciante
@app.route("/eliminarAnunciante", methods=["POST"])
def eliminarAnunciante():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "deleteanu"
    if request.method == "POST":
        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM anunciante WHERE id_anunciante like '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            # Eliminacion de anunciante
            cur.execute(
                """
                DELETE FROM anunciante WHERE id_anunciante like ('{0}');
                """.format(
                    id
                )
            )
            return_var = "menuadmin"
            conn.commit()
        else:
            flash("El anunciante ingresado no existe")
        cur.close()

    return redirect(url_for(return_var))


# Agregar anuncio
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
            return_var = "menuadmin"

            conn.commit()
        else:
            flash("El anunciante ingresado no existe")
        cur.close()

    return redirect(url_for(return_var))


# Modificar anuncio
@app.route("/modAnuncio", methods=["POST"])
def modAnuncio():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "modanuncio"
    if request.method == "POST":
        anuncioID = request.form["id"]
        # Sanitazacion de inputs
        anuncioID = anuncioID.replace("'", "")
        anuncioID = anuncioID.replace("--", "")
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
            SELECT * FROM anuncio WHERE id_anuncio = '{0}';
            """.format(
                id
            )
        )
        variable2 = cur.fetchone()

        if variable2:
            # Creacion de nuevo actor
            cur.execute(
                """
                UPDATE anuncio
                 SET id_anuncio='{0}',
                    id_anun='{1}',
                    url_ad='{2}',
                    texto='{3}'
                 WHERE id_anuncio like '{0}';
                """.format(
                    anuncioID, id, url_ad, descri
                )
            )
            conn.commit()
            return_var = "menuadmin"
        else:
            flash("El anuncio ingresado no existe")
        cur.close()

    return redirect(url_for(return_var))


# Eliminar un anuncio
@app.route("/eliminarAnuncio", methods=["POST"])
def eliminarAnuncio():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "deletead"
    if request.method == "POST":
        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM anuncio WHERE id_anuncio like '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            # Eliminacion de anunciante
            cur.execute(
                """
                DELETE FROM anuncio WHERE id_anuncio like ('{0}');
                """.format(
                    id
                )
            )
            return_var = "menuadmin"
            conn.commit()
        else:
            flash("El anuncio ingresado no existe")
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
                                return_var = "menuadmin"
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


# Modificar Trailer
@app.route("/modTrailer", methods=["POST"])
def modTrailer():
    return_var = "modtrailer"
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

        if existencia == None:
            flash("El trailer no existe")
        else:

            cur.execute(
                """
                UPDATE trailer
                SET id_trailer='{0}',
                    titulo='{1}',
                    genero_t='{2}',
                    categoria_t='{3}',
                    fechaestreno = '{4}',
                    director_t = '{5}',
                    actorprincipal = '{6}',
                    premiosganados = '{7}',
                    url='{8}',
                    summary='{9}',
                    ad='{10}',
                    tiempo_rep='{11}'
                WHERE id_trailer like '{0}';
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
            return_var = "menuadmin"
        cur.close()
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/eliminarTrailer", methods=["POST"])
def eliminarTrailer():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "deletetrailer"
    if request.method == "POST":
        id = request.form["id"]
        # Sanitazacion de inputs
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur.execute(
            """
            SELECT * FROM trailer WHERE id_trailer = '{0}';
            """.format(
                id
            )
        )
        variable = cur.fetchone()

        if variable:
            # Eliminacion de director
            cur.execute(
                """
                DELETE FROM trailer WHERE id_trailer like ('{0}');
                """.format(
                    id
                )
            )
            return_var = "cat"
            conn.commit()
        else:
            flash("El trailer ingresado no existe")
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
                cur.execute(
                    """
                    SELECT id_perfil FROM perfil p
                    LEFT JOIN usuario u ON p.id_usuario = u.id
                    WHERE u.correo LIKE '{0}'
                    """.format(
                        email
                    )
                )
                idactual = cur.fetchone()
                session["idactualperfil"] = idactual
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


# Eliminar un  trailer
@app.route("/Prueba", methods=["POST"])
def Prueba():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "cat"
    if request.method == "POST":
        if "idactualperfil" in session:
            idaingresar = session["idactualperfil"]

    return redirect(url_for(return_var))


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
def addanu():
    return render_template("addAnu.html")


# Eliminar anunciante
@app.route("/deleteanu")
def deleteanu():
    return render_template("DeleteAnunciante.html")


# Agregar director
@app.route("/adddir")
def add_director():
    return render_template("addDir.html")


# Eliminar director
@app.route("/deletedir")
def deletedir():
    return render_template("DeleteDirector.html")


# Agregar anuncio
@app.route("/addad")
def add_advertisment():
    return render_template("addAd.html")


# Delete anuncio
@app.route("/deletead")
def deletead():
    return render_template("DeleteAnuncio.html")


# Agregar actor
@app.route("/addactor")
def add_actor():
    return render_template("addAct.html")


@app.route("/deleteactor")
def deleteactor():
    return render_template("DeleteActor.html")


# Agregar trailer
@app.route("/addtrailer")
def addtrailer():
    return render_template("addTrailer.html")


# Eliminar trailer
@app.route("/deletecontent")
def deletecontent():
    return render_template("DeleteContent.html")


# Manejar contenido
@app.route("/manCon")
def manCon():
    return render_template("manejarContenido.html")


# Eliminar user
@app.route("/deleteuser")
def deleteuser():
    return render_template("DeleteUsuario.html")


# Modificar Actor
@app.route("/modact")
def modact():
    return render_template("modifyAct.html")


# Modificar Director
@app.route("/moddirector")
def moddirector():
    return render_template("modifyDirector.html")


# Modificar trailer
@app.route("/modtrailer")
def modtrailer():
    return render_template("modifyTrailer.html")


# Modificar contenido
@app.route("/modC")
def modC():
    return render_template("modificarContenido.html")


# Modificar anuncio
@app.route("/modanuncio")
def modanuncio():
    return render_template("modifyAnuncio.html")


# Modificar anuncio
@app.route("/modanunciante")
def modanunciante():
    return render_template("modificarAnunciante.html")


# Referencia: https://codeforgeek.com/render-html-file-in-flask/
if __name__ == "__main__":
    app.run(debug=True)
