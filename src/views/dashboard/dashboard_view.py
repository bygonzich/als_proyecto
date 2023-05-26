import flask
import flask_login
import sirope

from model.abonadodto import AbonadoDto


def get_blprint():
    dashboard = flask.blueprints.Blueprint("dashboard", __name__, url_prefix="/dashboard", template_folder="templates", static_folder="static")

    sirp = sirope.Sirope()

    return dashboard, sirp


dashboard_bp, srp = get_blprint()


@dashboard_bp.route("/dashboard", methods=["GET"])
@flask_login.login_required
def dashboard():
    datos = {
            "usuario" : flask_login.current_user.usuario
        }

    return flask.render_template("dashboard.html", **datos)
