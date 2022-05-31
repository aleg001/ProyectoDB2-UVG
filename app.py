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

sesionId = ""
IDActual = ""


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


app = Flask(__name__)
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


def ImpresionDic(primerAct):
    primerAct = primerAct.replace("[", "")
    primerAct = primerAct.replace("]", "")
    primerAct = primerAct.replace("(", "")
    primerAct = primerAct.replace(")", "")
    primerAct = primerAct.replace(",", "")
    primerAct = "Director y cantidad películas:", primerAct
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


def formato(repro):
    repro = repro.replace("[", "")
    repro = repro.replace("]", "")
    repro = repro.replace("(", "")
    repro = repro.replace(")", "")
    repro = repro.replace(",", "")
    return repro


# Variable global
contadorIntentosFallidos = 0


@app.route("/horasPico")
def horasPico():
    return render_template("horasPicos.html")


# Login de admin
@app.route("/adminLog", methods=["POST"])
def adminLog():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    global IDActual
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

                IDActual = idactual
                print("VALOR DE ID: ", IDActual)

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


# estadisticas
@app.route("/estadisticaHorasPico", methods=["POST"])
def estadisticaHorasPico():
    global IDActual
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
            WHERE s.tipo LIKE 'premium' OR s.tipo LIKE 'basic'
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
            where s.tipo like 'premium' or s.tipo like 'basic'
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

        ImpresionDic(primerAct)
        ImpresionDic(segundoAct)
        ImpresionDic(tercerAct)
        ImpresionDic(cuartoAct)
        ImpresionDic(QuintoAct)
        ImpresionDic(SextoAct)
        ImpresionDic(SepAct)
        ImpresionDic(OctAct)
        ImpresionDic(NovAct)
        ImpresionDic(DecAct)

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
        WHERE s.tipo LIKE 'premium'
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
    global IDActual
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

        tipo = request.form["tipoCuenta"]

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
        # Creacion de primer perfil
        cur.execute(
            """
            INSERT INTO suscripcion VALUES ('{0}', '{1}');
            """.format(
                IDActual, tipo
            )
        )

        cur.execute(
            """
            SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
            """
        )

        timestamp_bit = cur.fetchone()
        print(timestamp_bit)
        resultado = str(timestamp_bit[0])
        resultado = formato(resultado)
        IDActual = formato(IDActual)
        cur.execute(
            """
            UPDATE bitacora
                SET id_admin ='{0}'
                WHERE tiempo_mod = '{1}';
            """.format(
                IDActual, resultado
            )
        )
    conn.commit()
    cur.close()
    return redirect(url_for("login"))


# Eliminar un usuario
@app.route("/eliminarUsuario", methods=["POST"])
def eliminarUsuario():
    global IDActual
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
                )
            )

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
    session.pop("idactualperfil", None)
    return redirect(url_for("login"))


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


# Agregar un nuevo director
@app.route("/agregarDirector", methods=["POST"])
def agregarDirector():
    global IDActual
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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
    global IDActual
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
                )
            )
            return_var = "menuadmin"
            conn.commit()
        cur.close()

    return redirect(url_for(return_var))


# Modificar un anunciante
@app.route("/modAnunciante", methods=["POST"])
def modAnunciante():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return_var = "modanunciante"
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
            # Modificacion de anunciante
            cur.execute(
                """
                UPDATE anunciante
                 SET id_anunciante='{0}',
                    nombre='{1}'
                 WHERE id_anunciante like '{0}';
                """.format(
                    id, name
                )
            )
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
                )
            )
            return_var = "menuadmin"
            conn.commit()
        else:
            flash("El anunciante no existe")
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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
                anuncioID
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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

            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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
    return_var = "addtrailer"
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

                                cur.execute(
                                    """
                                    SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                                    """
                                )

                                timestamp_bit = cur.fetchone()
                                print(timestamp_bit)
                                resultado = str(timestamp_bit[0])
                                resultado = formato(resultado)
                                IDActual = str(IDActual[0])
                                IDActual = formato(IDActual)
                                cur.execute(
                                    """
                                    UPDATE bitacora
                                        SET id_admin ='{0}'
                                        WHERE tiempo_mod = '{1}';
                                    """.format(
                                        IDActual, resultado
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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
            cur.execute(
                """
                SELECT tiempo_mod FROM bitacora b ORDER BY tiempo_mod desc limit 1;
                """
            )

            timestamp_bit = cur.fetchone()
            print(timestamp_bit)
            resultado = str(timestamp_bit[0])
            resultado = formato(resultado)
            IDActual = str(IDActual[0])
            IDActual = formato(IDActual)
            cur.execute(
                """
                UPDATE bitacora
                    SET id_admin ='{0}'
                    WHERE tiempo_mod = '{1}';
                """.format(
                    IDActual, resultado
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
                IDActual = idactual
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
@app.route("/m1", methods=["GET", "POST"])
def m1():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra1", "idad1", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m2", methods=["GET", "POST"])
def m2():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra2", "idad4", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m3", methods=["GET", "POST"])
def m3():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra3", "idad3", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m4", methods=["GET", "POST"])
def m4():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra4", "idad4", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m5", methods=["GET", "POST"])
def m5():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra5", "idad5", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m6", methods=["GET", "POST"])
def m6():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra6", "idad6", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m7", methods=["GET", "POST"])
def m7():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra7", "idad7", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m8", methods=["GET", "POST"])
def m8():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra8", "idad8", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m9", methods=["GET", "POST"])
def m9():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra9", "idad9", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m10", methods=["GET", "POST"])
def m10():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:
            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra10", "idad1", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m11", methods=["GET", "POST"])
def m11():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:
            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra11", "idad1", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m12", methods=["GET", "POST"])
def m12():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra12", "idad2", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m13", methods=["GET", "POST"])
def m13():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra13", "idad3", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m14", methods=["GET", "POST"])
def m14():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra14", "idad4", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m15", methods=["GET", "POST"])
def m15():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra15", "idad5", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


# Eliminar un  trailer
@app.route("/m16", methods=["GET", "POST"])
def m16():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    return_var = "cat"
    if request.method == "GET":
        if "idactualperfil" in session:

            idreproduccion = IDIntentoFallido()
            fechareproducida = FechaActual()
            cur.execute(
                """
                INSERT INTO reproduccion VALUES ('{0}', '{1}', '{2}','{3}', '{4}');
                """.format(
                    idreproduccion, idActual1, "idtra16", "idad16", fechareproducida
                )
            )
            conn.commit()
            return_var = "cat"

            flash("Reproducido con éxito!")
    return redirect(url_for(return_var))


@app.route("/busTi", methods=["GET", "POST"])
def busTi():
    if request.method == "POST":
        id = request.form["id"]
        id = id.replace("'", "")
        id = id.replace("--", "")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            SELECT * FROM trailer t WHERE titulo like '{0}';
            INSERT INTO palabras_busqueda
            VALUES ('{0}');
            """.format(
                id
            )
        )
        busTitulo = cur.fetchall()
        return render_template("busquedaTitulo.html", lista=busTitulo)


# Busqueda titulo
@app.route("/busquedatitulo")
def busquedatitulo():
    return render_template("busquedaTitulo.html")


@app.route("/busAc", methods=["GET", "POST"])
def busAc():
    if request.method == "POST":
        id = request.form["id"]
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            SELECT * FROM trailer t
            LEFT JOIN actor a ON t.actorprincipal = a.id_actor
            WHERE a.nombre like '{0}';
            INSERT INTO palabras_busqueda
            VALUES ('{0}');
            """.format(
                id
            )
        )
        busTitulo = cur.fetchall()
        return render_template("busquedaActor.html", lista=busTitulo)


# Busqueda titulo
@app.route("/busquedaActor")
def busquedaActor():
    return render_template("busquedaActor.html")


@app.route("/busG", methods=["GET", "POST"])
def busG():
    if request.method == "POST":
        id = request.form["id"]
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            SELECT * FROM trailer t 
            LEFT JOIN genero g ON t.genero_t = g.id_genero
            WHERE g.nombregen like '{0}';
            INSERT INTO palabras_busqueda
            VALUES ('{0}');
            """.format(
                id
            )
        )
        busTitulo = cur.fetchall()
        return render_template("busquedaGenero.html", lista=busTitulo)


@app.route("/busBit", methods=["GET", "POST"])
def busBit():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM bitacora order by tiempo_mod desc
        """
    )
    bitacorax = cur.fetchall()
    return render_template("bitacoras.html", lista=bitacorax)


@app.route("/busD", methods=["GET", "POST"])
def busD():
    if request.method == "POST":
        id = request.form["id"]
        id = id.replace("'", "")
        id = id.replace("--", "")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            SELECT * FROM trailer t 
            LEFT JOIN director d ON t.director_t = d.id_director
            WHERE d.nombre like '{0}';
            INSERT INTO palabras_busqueda
            VALUES ('{0}');
            """.format(
                id
            )
        )
        busTitulo = cur.fetchall()
        return render_template("busquedaDirector.html", lista=busTitulo)


# Busqueda titulo
@app.route("/busquedadirec")
def busquedadirec():
    return render_template("busquedaDirector.html")


# Hub de busqueda
@app.route("/menuTabla")
def menuTabla():
    return render_template("tabla.html")


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


# Agregar anuncio
@app.route("/tipoCuenta")
def tipoCuenta():
    return render_template("accountType.html")


@app.route("/tipoCuenta1", methods=["GET", "POST"])
def tipoCuenta1():
    if request.method == "POST":
        id = request.form["tipoCuenta"]

        idaingresar = session["idactualperfil"]

        idActual1 = str(idaingresar[0])
        idActual1 = idActual1.replace("'", "")
        idActual1 = idActual1.replace("[", "")
        idActual1 = idActual1.replace("]", "")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
                UPDATE suscripcion
                 SET tipo='{1}'
                 WHERE id_user LIKE '{0}';
            """.format(
                idActual1, id
            )
        )
        conn.commit()
        cur.close()
        return render_template("catalogue.html")


# Agregar anuncio
@app.route("/manejarPerfil")
def manejarPerfil():
    return render_template("accountType.html")


@app.route("/tablaPerfil")
def tablaPerfil():
    idaingresar = session["idactualperfil"]
    idActual1 = str(idaingresar[0])
    idActual1 = idActual1.replace("'", "")
    idActual1 = idActual1.replace("[", "")
    idActual1 = idActual1.replace("]", "")
    print(idActual1)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
            select p.id_perfil, p.nombre 
            from perfil p 
            left join usuario u on p.id_usuario = u.id 
            where p.id_usuario in (
                select u2.id 
                from perfil p2 
                left join usuario u2 on p2.id_usuario = u2.id 
                where p2.id_perfil like '{0}'
            );
            
        """.format(
            idActual1
        )
    )
    PerfilesActuales = cur.fetchall()
    return render_template("tablaPerfiles.html", lista=PerfilesActuales)


@app.route("/manDel", methods=["GET", "POST"])
def manDel():
    if request.method == "POST":
        idaingresar = request.form["idDel"]
        idaingresar = idaingresar.replace("'", "")
        idaingresar = idaingresar.replace("--", "")
        print(idaingresar)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """ 
            delete
            from perfil p 
            where p.id_perfil like '{0}'
        """.format(
                idaingresar
            )
        )

        flash("Eliminado!")
        conn.commit()
        cur.close()
    return render_template("catalogue.html")


@app.route("/manPer", methods=["GET", "POST"])
def manPer():
    if request.method == "POST":

        valorRandom = IDUsuario()
        # id = request.form["idEliminar"]
        # id = id.replace("'", "")
        # id = id.replace("--", "")
        perfil = request.form["nombrePerfil"]
        perfil = perfil.replace("'", "")
        perfil = perfil.replace("--", "")

        idaingresar = session["idactualperfil"]
        idActual1 = str(idaingresar[0])
        idActual1 = idActual1.replace("'", "")
        idActual1 = idActual1.replace("[", "")
        idActual1 = idActual1.replace("]", "")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            select s.tipo 
            from suscripcion s 
            left join perfil p on s.id_user = p.id_usuario
            where p.id_perfil like '{0}' and s.tipo like 'free'
        
        """.format(
                idActual1
            )
        )
        free = cur.fetchall()

        free = " ".join([" ".join([str(c) for c in lst]) for lst in free])

        cur.execute(
            """
            select s.tipo 
            from suscripcion s 
            left join perfil p on s.id_user = p.id_usuario
            where p.id_perfil like '{0}' and s.tipo like 'basic'
        
        """.format(
                idActual1
            )
        )
        basic = cur.fetchall()
        basic = " ".join([" ".join([str(c) for c in lst]) for lst in basic])

        cur.execute(
            """
            select s.tipo 
            from suscripcion s 
            left join perfil p on s.id_user = p.id_usuario
            where p.id_perfil like '{0}' and s.tipo like 'premium'
        
        """.format(
                idActual1
            )
        )
        premium = cur.fetchall()
        premium = " ".join([" ".join([str(c) for c in lst]) for lst in premium])
        if free == "free":
            flash("Cambia de tipo de cuenta para agregar perfiles!!")

        if basic == "basic":
            cur.execute(
                """
                select count(*) as cont
                from perfil p 
                left join usuario u on p.id_usuario = u.id 
                where p.id_usuario in (
                    select u2.id 
                    from perfil p2 
                    left join usuario u2 on p2.id_usuario = u2.id 
                    where p2.id_perfil like '{0}'
                ) having count(*) <= 3
        
            """.format(
                    idActual1
                )
            )
            basico = cur.fetchall()
            if basico:
                cur.execute(
                    """
                    select u2.id 
                    from perfil p2 
                    left join usuario u2 on p2.id_usuario = u2.id 
                    where p2.id_perfil like '{0}'
            
                """.format(
                        idActual1
                    )
                )
                id_actualusuario = cur.fetchall()
                id_actualusuario = str(id_actualusuario[0])
                id_actualusuario = id_actualusuario.replace("'", "")
                id_actualusuario = id_actualusuario.replace("[", "")
                id_actualusuario = id_actualusuario.replace("]", "")
                cur.execute(
                    """
                insert into perfil values('{0}', '{1}', '{2}', 'false');
            
                """.format(
                        valorRandom, id_actualusuario, perfil
                    )
                )

        if premium == "premium":
            cur.execute(
                """
                select count(*) as cont
                from perfil p 
                left join usuario u on p.id_usuario = u.id 
                where p.id_usuario in (
                    select u2.id 
                    from perfil p2 
                    left join usuario u2 on p2.id_usuario = u2.id 
                    where p2.id_perfil like '{0}'
                ) having count(*) <= 7
        
            """.format(
                    perfil
                )
            )
            premio = cur.fetchall()
            if premio:
                cur.execute(
                    """
                    select u2.id 
                    from perfil p2 
                    left join usuario u2 on p2.id_usuario = u2.id 
                    where p2.id_perfil like '{0}'
            
                """.format(
                        idActual1
                    )
                )
                id_actualusuario = cur.fetchall()
                id_actualusuario = str(id_actualusuario[0])
                id_actualusuario = id_actualusuario.replace("'", "")
                id_actualusuario = id_actualusuario.replace("[", "")
                id_actualusuario = id_actualusuario.replace("]", "")

                cur.execute(
                    """
                insert into perfil values('{0}', '{1}', '{2}', 'false');
            
                """.format(
                        valorRandom, id_actualusuario, perfil
                    )
                )

        conn.commit()
        cur.close()
    return render_template("tablaPerfiles.html")


@app.route("/favs", methods=["GET", "POST"])
def favs():
    if request.method == "POST":

        id = request.form["idvid"]
        print(id)
        id = id.replace("'", "")
        id = id.replace("--", "")
        idaingresar = session["idactualperfil"]

        idActual1 = str(idaingresar[0])
        idActual1 = idActual1.replace("'", "")
        idActual1 = idActual1.replace("[", "")
        idActual1 = idActual1.replace("]", "")
        idreproduccion = IDIntentoFallido()
        fechareproducida = FechaActual()

        # Jalar ID de perfil
        if "idactualperfil" in session:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                    INSERT INTO favoritos VALUES('{0}','{1}');
                """.format(
                    idActual1, id
                )
            )
            conn.commit()

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                    INSERT INTO reproduccion VALUES ('{2}', '{3}', '{4}','{5}', '{6}');
                """.format(
                    idreproduccion, idActual1, id, "idad1", fechareproducida
                )
            )
            conn.commit()
            cur.close()

        else:
            print("no tengo id...")

        return render_template("catalogue.html")


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
    return render_template("modifyAnunciante.html")


@app.route("/configureishon")
def configureishon():
    return render_template("configuracion.html")


@app.route("/config1")
def config1():
    return render_template("configuracion.html")


# Nueva reporteria - renders
@app.route("/reporteria2")
def reporteria2():
    return render_template("reporteria2.html")


# Top 5 admins
@app.route("/topAdmins")
def top5Admins():
    return render_template("top5Admins.html")


# Top 5 contenido
@app.route("/topCont")
def top5Cont():
    return render_template("top5Contenido.html")


# Top 10 terminos
@app.route("/topTerminos")
def top10Terminos():
    return render_template("top10Terminos.html")


# Top 20 visto
@app.route("/topNoTerminado")
def top20NoTerminado():
    return render_template("top20Visto.html")


# Reporteria funciones

# top 5
@app.route("/contenidoDado", methods=["POST"])
def contenidoVistoMes():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cur.execute(
            """
             
        """.format()
        )
        actoresdirectores = cur.fetchall()
        flash(actoresdirectores)
        conn.commit()
        cur.close()
    return render_template("top5Contenido.html")


# top terminos
@app.route("/terminosBuscados", methods=["POST"])
def terminosBuscados():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cur.execute(
            """
        select top10terms();
        """
        )
        actoresdirectores = cur.fetchall()
        flash(actoresdirectores)
        conn.commit()
        cur.close()
    return render_template("top10Terminos.html")


@app.route("/adminMod", methods=["POST"])
def adminModificacion():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == "POST":
        fecha1 = request.form["fecha1"]
        fecha2 = request.form["fecha2"]
        cur.execute(
            """
            select top5admin('{0}','{1}');
        """.format(
                fecha1, fecha2
            )
        )
        actoresdirectores = cur.fetchall()

        # [[datetime.time(21, 0)], [datetime.time(20, 0)], [datetime.time(16, 0)]]
        primerAct = str(actoresdirectores[0])
        segundoAct = str(actoresdirectores[1])
        tercerAct = str(actoresdirectores[2])
        cuartoAct = str(actoresdirectores[3])
        QuintoAct = str(actoresdirectores[4])

        flash(primerAct)
        flash(segundoAct)
        flash(tercerAct)
        flash(cuartoAct)
        flash(QuintoAct)

        conn.commit()
        cur.close()
    return render_template("top5Admins.html")


# Top 20 peli sin terminar
@app.route("/peliFin", methods=["POST"])
def peliSinTerminar():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        fecha1 = request.form["fecha1"]
        fecha2 = request.form["fecha2"]
        cur.execute(
            """
        select top20pelis('{0}','{1}')
        """.format(
                fecha1, fecha2
            )
        )
        actoresdirectores = cur.fetchall()
        flash(actoresdirectores)
        conn.commit()
        cur.close()
    return render_template("top20Visto.html")


# Continuar viendo
@app.route("/continuarViendo", methods=["GET", "POST"])
def continuarViendo():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        select distinct t.titulo 
        from reproduccion r 
        left join trailer t on r.id_vid = t.id_trailer 
        where r.fecha_terminado is null
        and r.id_per like 'idper4'
        order by t.titulo;
        """
    )
    enProgreso = cur.fetchall()
    return render_template("continuarViendo.html", lista=enProgreso)


# Sacar lista de usuarios
@app.route("/listaTotal", methods=["GET", "POST"])
def listaTotal():
    if request.method == "POST":
        idaingresar = session["idactualperfil"]
        idActual1 = str(idaingresar[0])
        idActual1 = idActual1.replace("'", "")
        idActual1 = idActual1.replace("[", "")
        idActual1 = idActual1.replace("]", "")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            select distinct t.titulo 
            from reproduccion r 
            left join trailer t on r.id_vid = t.id_trailer 
            where r.fecha_terminado is null
            and r.id_per like '{0}'
            order by t.titulo;
            """.format(
                idActual1
            )
        )
        listacompleta = cur.fetchall()
        return render_template("continuarViendo.html", lista=listacompleta)


# Terminar de ver
@app.route("/actualizarLista", methods=["GET", "POST"])
def actualizarLista():
    if request.method == "POST":
        flash("Has terminado de ver esta peli!")
        titulo = request.form["titulo"]
        print(titulo)
        titulo = titulo.replace("'", "")
        titulo = titulo.replace("--", "")
        idaingresar = session["idactualperfil"]
        idActual1 = str(idaingresar[0])
        idActual1 = idActual1.replace("'", "")
        idActual1 = idActual1.replace("[", "")
        idActual1 = idActual1.replace("]", "")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            update 
            reproduccion 
            set 
            fecha_terminado = CURRENT_TIMESTAMP
            where reproduccion.id_rep in(
            select id_rep from reproduccion r,trailer 
            where r.id_vid = trailer.id_trailer
            and r.id_per like '{0}' and trailer.titulo like '{1}'
            );
            """.format(
                idActual1, titulo
            )
        )
        conn.commit()
        cur.close()
        idaingresar = session["idactualperfil"]
        idActual1 = str(idaingresar[0])
        idActual1 = idActual1.replace("'", "")
        idActual1 = idActual1.replace("[", "")
        idActual1 = idActual1.replace("]", "")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            select distinct t.titulo 
            from reproduccion r 
            left join trailer t on r.id_vid = t.id_trailer 
            where r.fecha_terminado is null
            and r.id_per like '{0}'
            order by t.titulo;
            """.format(
                idActual1
            )
        )
        listacompleta = cur.fetchall()
        conn.commit()
        cur.close()

        return render_template("continuarViendo.html", lista=listacompleta)


# Simulaciones
@app.route("/Simulaciones")
def Simulaciones():
    return render_template("Simulaciones.html")


# simulaciones peliculas
@app.route("/simPeli")
def simPeli():
    return render_template("simPeli.html")


@app.route("/simularpeliculas", methods=["POST"])
def simularpeliculas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cant = request.form["cant"]
        cur.execute(
            """
        select peli_simulacion('{0}')
        """.format(
                cant
            )
        )
        flash("Se ha agregado a la base de datos")
        conn.commit()
        cur.close()
    return render_template("simPeli.html")


# simulaciones usuarios
@app.route("/simUser")
def simUser():
    return render_template("simUsuarios.html")


@app.route("/simularusuarios", methods=["POST"])
def simularusuarios():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cant = request.form["cant"]
        cur.execute(
            """
        select usuario_simulacion('{0}')
        """.format(
                cant
            )
        )
        flash("Se ha agregado a la base de datos")
        conn.commit()
        cur.close()
    return render_template("simUsuarios.html")


# simulaciones visualizaciones
@app.route("/simVis")
def simVis():
    return render_template("simVisual.html")


@app.route("/simularvisualizaciones", methods=["POST"])
def simularvisualizaciones():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cant = request.form["cant"]
        fecha1 = request.form["dateI"]
        cur.execute(
            """
        select repros_simulacion('{0}','{1}');
        """.format(
                cant, fecha1
            )
        )
        flash("Se ha agregado a la base de datos")
        conn.commit()
        cur.close()
    return render_template("simVisual.html")


# Continuar viendo
@app.route("/Mantenimiento", methods=["GET", "POST"])
def Mantenimiento():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        select * from usuario
        where isadmin like 'false';
        """
    )
    manta = cur.fetchall()
    return render_template("mantenimiento.html", lista=manta)


@app.route("/mantenimiento1", methods=["GET", "POST"])
def mantenimiento1():
    if request.method == "POST":
        user = request.form["user"]
        user = user.replace("'", "")
        user = user.replace("--", "")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
        update usuario set isadmin = 'true'
            where id like '{0}'
            """.format(
                user
            )
        )
        conn.commit()
        cur.close()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            select * from usuario
            where isadmin like 'false';
            """
        )
        manta = cur.fetchall()
    return render_template("mantenimiento.html", lista=manta)


# Referencia: https://codeforgeek.com/render-html-file-in-flask/
if __name__ == "__main__":
    app.run(debug=True)
