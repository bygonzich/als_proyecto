import flask
import sirope
import json
import flask_login

from model.abonadodto import AbonadoDto
from model.asistenciadto import AsistenciaDto
from model.rutinadto import RutinaDto
import views.dashboard.dashboard_view as dashboard_view
import views.asistencia.asistencia_view as asistencia_view
import views.rutina.rutina_view as rutina_view


def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    fapp = flask.Flask(__name__, instance_relative_config=True)
    sirp = sirope.Sirope()

    fapp.config.from_file("config.json", load=json.load)
    lmanager.init_app(fapp)
    fapp.register_blueprint(dashboard_view.dashboard_bp)
    fapp.register_blueprint(asistencia_view.asistencia_bp)
    fapp.register_blueprint(rutina_view.rutina_bp)
    return fapp, lmanager, sirp

app, lm, srp = create_app()


@lm.user_loader
def user_loader(usuario):
    return AbonadoDto.find(srp, usuario)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")



@app.route("/")
def index():
    #key = srp.load_all_keys(AsistenciaDto)
    #for k in key:
    #    srp.delete(k)

    usuario = AbonadoDto.current_user()

    datos = {
        "usuario": usuario
    }

    if usuario != None:
        return flask.render_template("dashboard.html", **datos)
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    usuarioLogin = flask.request.form["usuarioLogin"].strip()
    contraLogin = flask.request.form["contraLogin"].strip()

    if not usuarioLogin or not contraLogin:
        flask.flash("Rellena todos los campos")
        return flask.redirect("/")
        
    usuario = AbonadoDto.find(srp, usuarioLogin)

    if not usuario or not usuario.check_password(contraLogin):
        flask.flash("Usuario incorrecto")
        return flask.redirect("/")

    flask_login.login_user(usuario)
    return flask.redirect("/dashboard")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    flask.flash("Sesión cerrada")
    return flask.redirect("/")


@app.route("/register", methods=["POST"])
def register():
    usuarioRegister = flask.request.form["usuarioRegister"].strip()
    contraRegister = flask.request.form["contraRegister"].strip()

    if not usuarioRegister or not contraRegister:
        flask.flash("Rellena todos los campos")
        return flask.redirect("/")

    usuario = AbonadoDto.find(srp, usuarioRegister)

    if not usuario:
        usuario = AbonadoDto(usuarioRegister, contraRegister)
        srp.save(usuario)
        flask.flash("Usuario registrado")
        return flask.redirect("/")
    else:
        flask.flash("Nombre de usuario en uso")
        return flask.redirect("/")


@app.route("/dashboard", methods=["GET"])
@flask_login.login_required
def dashboard():
    datos = {
            "usuario" : flask_login.current_user.usuario
        }

    return flask.render_template("dashboard.html", **datos)


@app.route("/asistencia", methods=["GET", "POST"])
@flask_login.login_required
def asistencia():
    if flask.request.method == "GET":
        asistencias = list(srp.load_all(AsistenciaDto))
        asistencias = [a for a in asistencias if a.usuario == flask_login.current_user.usuario]

        datos = {
            "asistencias": asistencias
        }

        return flask.render_template("asistencia.html", **datos)

    else:
        srp.save(AsistenciaDto(flask_login.current_user.usuario))
        return flask.redirect("/asistencia")

@app.route("/asistencia/delete", methods=["POST"])
@flask_login.login_required
def asistencia_delete():
    asist_id = flask.request.form["asistencia_id"]
    for asistencia in srp.load_all(AsistenciaDto):
        if str(asistencia.id) == str(asist_id):
            oid = asistencia.__dict__[srp.OID_ID]
            srp.delete(oid)
    return flask.redirect("/asistencia")


@app.route("/rutina", methods=["GET", "POST"])
@flask_login.login_required
def rutina():
    if flask.request.method == "GET":
        rutinas = list(srp.load_all(RutinaDto))

        datos = {
            "rutinas": rutinas
        }

        return flask.render_template("rutina.html", **datos)

    else:
        numEjers = flask.request.form["numEjers"].strip()
        musculo = flask.request.form["musculo"].strip()

    if not numEjers or not musculo:
        flask.flash("Rellena todos los campos")
        return flask.redirect("/rutina")

    srp.save(RutinaDto(flask_login.current_user.usuario, numEjers, musculo))
    return flask.redirect("/rutina")
