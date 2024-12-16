from application.extension import db, app, login
from datetime import datetime
from flask_login import UserMixin
from flask import redirect, url_for, flash
from itsdangerous.url_safe import URLSafeTimedSerializer as serializer

@login.user_loader
def load_user(Id):
    return Users.query.get(Id)

def load_tokens(token):
    try:
        user_id = Users.verify_token(token)
        if user_id:
            return Users.query.get(user_id)
        else:
            flash(f"Your Token is Invalid or has expired", "error")
    except Exception as e:
        flash(f"An Error Occurred while verify token", "error")
        print(f"Token Verification error {e}")
    return None

@login.unauthorized_handler
def unauthorized():
    flash(f'You need to login first!!', 'error')
    return redirect(url_for('auth_ctl.login_page'))

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    Id = db.Column(db.Integer(), primary_key=True)
    Fullnames = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Phone = db.Column(db.String(14), nullable=False)
    PostalAddress = db.Column(db.String(100), nullable=False)
    PhysicalAddress = db.Column(db.String(200), nullable=False)
    County = db.Column(db.String(50), nullable=False)
    DOB = db.Column(db.DateTime(), nullable=False)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    ProfilePic = db.Column(db.String(255), nullable=False, default=app.config['DEFAULT_PROFILE_IMAGE'])
    CreatedOn = db.Column(db.DateTime(), default=datetime.utcnow)

    def get_id(self):
        return str(self.Id)

    def generate_token(self, expire_sec=600):
        serial = serializer(app.config["SECRET_KEY"], expire_sec)
        token = serial.dumps({'user_id': self.Id}, salt=app.config["SECURITY_PASSWORD_SALT"])
        return token

    @staticmethod
    def verify_token(token, expire_sec=600):
        serial = serializer(app.config["SECRET_KEY"])
        try:
            data = serial.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expire_sec)['user_id']
            return data
        except Exception as e:
            print('Token is Invalid or has already Expired!')
            return None

    @staticmethod
    def velidate_token(token, expire_sec=300):
        serial = serializer(app.config["SECRET_KEY"])
        try:
            user_id = serial.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expire_sec)['user_id']
            return Users.query.get(user_id)
        except Exception as e:
            print('Token is Invalid or has already Expired!')
            return None


    #isenabled = db.Column("is_enabled", db.Boolean, default=True)
    #isactive = True
    #isanonymous = False
    #authenticated = False

class Course(db.Model):
    Id = db.Column(db.Integer(), primary_key=True)
    Code = db.Column(db.String(100), nullable=False, unique=True)
    Name = db.Column(db.String(200), nullable=False)
    CreatedOn = db.Column(db.DateTime(), default=datetime.utcnow)

    Students = db.relationship("Student", back_populates = "Courses")
    Books = db.relationship("Book", back_populates="Courses")

class Student(db.Model):
    Id = db.Column(db.Integer(), primary_key=True)
    AdmNo = db.Column(db.String(50), nullable=False, unique=True)
    FullNames = db.Column(db.String(100), nullable=False)
    EmailAddress = db.Column(db.String(255), nullable=False, unique=True)
    PhoneNumber = db.Column(db.String(15), nullable = False)
    County = db.Column(db.String(100), nullable=False)
    CourseId = db.Column(db.ForeignKey("course.Id"))
    StudentProfile = db.Column(db.String(255), nullable=False)
    CreatedOn = db.Column(db.DateTime(), default=datetime.utcnow)

    Courses = db.relationship("Course", back_populates = "Students")

class Book(db.Model):
    Id = db.Column(db.Integer(), primary_key = True)
    Tittle = db.Column(db.String(100), nullable=False)
    Author = db.Column(db.String(100), nullable=100)
    ISBN = db.Column(db.String(30), nullable=False)
    PublishedOn = db.Column(db.DateTime(), nullable=False)
    CourseId = db.Column(db.ForeignKey("course.Id"), nullable=False)
    BookPoster = db.Column(db.String(255), nullable=False)
    CreatedOn = db.Column(db.DateTime(), default=datetime.utcnow)

    Courses = db.relationship("Course", back_populates="Books")


