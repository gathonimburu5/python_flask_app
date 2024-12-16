from flask import Blueprint, render_template, redirect, url_for, session, g, flash
from application.extension import db
from flask_login import login_required, current_user
from application.models import load_tokens

dash_ctrl = Blueprint('dash_ctrl', __name__)

# @dash_ctrl.before_request
# def load_logged_user():
#     token = session.get('auth_token')
#     if token:
#         user = load_tokens(token)
#         if user:
#             g.user = user
#         else:
#             flash(f'Session Expired, You need to loggin again!')
#             return redirect(url_for('auth_ctl.login_page'))
#     else:
#         g.user = None

@dash_ctrl.route("/", methods=["GET", "POST"])
@login_required
def dashboard_page():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_ctl.login_page'))

    return render_template("index.html")