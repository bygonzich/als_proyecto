import flask
import flask_login
import sirope

from model.abonadodto import AbonadoDto
from model.asistenciadto import AsistenciaDto


def get_blprint():
    asistencia = flask.blueprints.Blueprint("asistencia", __name__, url_prefix="/asistencia", template_folder="templates", static_folder="static")

    sirp = sirope.Sirope()

    return asistencia, sirp


asistencia_bp, srp = get_blprint()



@asistencia_bp.route("/asistencia", methods=["GET", "POST"])
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
