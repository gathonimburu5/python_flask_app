from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterUser(FlaskForm):
    full_names = StringField(label="Full Names", validators=[DataRequired(), Length(max=100)])
    email_address = StringField(label="Email Address", validators=[DataRequired(), Email(), Length(max=255)] )
    phone_number = StringField(label="Phone Number", validators=[DataRequired(), Length(max=15)])
    postal_address = StringField(label="Postal Address", validators=[DataRequired()])
    physical_address = StringField(label="Physical Address", validators=[DataRequired()])
    county = StringField(label="County", validators=[DataRequired()])
    date_birth = DateField(label="Date Of Birth", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=8, max=15)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(max=15, min=8)])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo(password)] )
    submit_button = SubmitField(label="Sign Up")

class LoginUser(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=8, max=15)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(max=15, min=8)])
    submit_button = SubmitField(label="Sign In")

class BookForm(FlaskForm):
    tittle = StringField("Tittle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    isbn = StringField("ISBN", validators=[DataRequired()])
    published_on = DateField("Published On", validators=[DataRequired()])
    course = SelectField("Course", choices=[], coerce=int, validators=[DataRequired()])
    submit_button = SubmitField("Create Book")
    close_button = SubmitField("Close")


