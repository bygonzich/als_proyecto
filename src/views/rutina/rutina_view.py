import flask
import flask_login
import sirope

from model.abonadodto import AbonadoDto
from model.asistenciadto import AsistenciaDto
from model.rutinadto import RutinaDto


def get_blprint():
    rutina = flask.blueprints.Blueprint("rutina", __name__, url_prefix="/rutina", template_folder="templates", static_folder="static")

    sirp = sirope.Sirope()

    return rutina, sirp


rutina_bp, srp = get_blprint()



@rutina_bp.route("/rutina", methods=["GET", "POST"])
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
