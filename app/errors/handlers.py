from flask import Blueprint, render_template

bp = Blueprint('errors', __name__)


# Route for handling the 404
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


# Route for handling the 401
@bp.app_errorhandler(401)
def invalid_login(e):
    return render_template('error/401.html'), 401
