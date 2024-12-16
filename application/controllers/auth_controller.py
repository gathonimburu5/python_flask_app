from flask import Blueprint, redirect, request, url_for, render_template, flash, session
from application.services.auth_service import Authentication_Service
from application.models import Users
from application.extension import bcrypt, db, mail, app
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import os

auth_ctl = Blueprint('auth_ctl', __name__)
auth_service = Authentication_Service()

@auth_ctl.route("/", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dash_ctrl.dashboard_page'))

    data = request.form
    if request.method == "POST":
        user = Users.query.filter_by(Username = data.get('username')).first()
        if user and bcrypt.check_password_hash(user.Password, data.get('password')):
            login_user(user)
            token = user.generate_token()
            session['auth_token'] = token

            flash(f'successfully logged in.', 'success')
            return redirect(url_for('dash_ctrl.dashboard_page'))
        else:
            flash(f'failed to log in, please check your credentials', 'error')
            return redirect(url_for('auth_ctl.login_page'))

    return render_template("auth/login.html")

@auth_ctl.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('dash_ctrl.dashboard_page'))

    data = request.form
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        flash(f'password must be equal to confirm password, please check your password', 'error')
        return redirect(url_for('auth_ctl.register_page'))

    if request.method == "POST":
        auth_service.RegisterUser(data)
        flash(f'successfully registered', 'success')
        return redirect(url_for('auth_ctl.login_page'))

    return render_template("auth/register.html")

@auth_ctl.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_ctl.login_page'))

def send_email(user):
    token = user.generate_token()
    msg = Message('Change Password Request', sender='noreply@gathoni.com', recipients=[user.Email])
    msg.body = f"""  Click the following link to reset your password:
        {url_for('auth_ctl.change_password', token=token, _external=True)}

        Ignore this email if you did not request any Password Reset!!
    """
    mail.send(msg)

@auth_ctl.route("/reset", methods=["GET", "POST"])
def reset_page():
    if current_user.is_authenticated:
        return redirect(url_for('dash_ctrl.dashboard_page'))

    if request.method == "POST":
        data = request.form
        email = data.get('email_address')
        user = Users.query.filter_by(Email = email).first()
        if user:
            send_email(user)
            flash(f"An Email with Reset Password Instruction have successfully been sent, Please check your email to reset password?", "success")
            return redirect(url_for('auth_ctl.login_page'))
        else:
            flash(f"{email} not found, Please Register", "error")
            return redirect(url_for('auth_ctl.register_page'))

    return render_template('auth/reset.html')


@auth_ctl.route("/reset_password/<token>", methods=["GET", "POST"])
def change_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dash_ctrl.dashboard_page'))

    user = Users.velidate_token(token)
    if not user:
        flash(f"Invalid or Expired Token, Please Try again", "error")
        return redirect(url_for('auth_ctl.reset_page'))

    if request.method == "POST":
        data = request.form
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            flash(f"Password and Confirm Password must be equal", "error")
            return redirect(url_for('auth_ctl.change_password'))

        hashed_password =bcrypt.generate_password_hash(password).decode("utf-8")
        user.Password = hashed_password
        db.session.commit()
        flash(f"Password Changed Successfully, You can Now Logg-in", "success")
        return redirect(url_for('auth_ctl.login_page'))

    return render_template("auth/change_password.html")

# function to upload image
def upload_image(profile_pic):
    pic_namme = profile_pic.filename
    pic_path = os.path.join(app.root_path, 'static/assets/images/users/', pic_namme)
    profile_pic.save(pic_path)
    return pic_namme

@auth_ctl.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_ctl.login_page'))

    if request.method == "POST":
        data = request.form
        image = request.files.get('profile_image')
        if image is None:
            flash('please upload image?', 'error')
            return redirect(url_for('auth_ctl.profile_page'))

        current_user.ProfilePic = upload_image(image)
        current_user.Fullnames = data.get('full_names')
        current_user.Phone = data.get('phone_number')
        current_user.DOB = data.get('dob')
        current_user.County = data.get('user_county')
        current_user.PostalAddress = data.get('postal_address')
        current_user.PhysicalAddress = data.get('physical_address')
        db.session.flush()
        db.session.commit()
        flash(f"successfully updated profile details.", "success")
        return redirect(url_for('auth_ctl.profile_page'))

    return render_template("auth/profile.html")


