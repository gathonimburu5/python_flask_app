from application.extension import db, bcrypt
from application.models import Users


class Authentication_Service():
    def RegisterUser(self, form):
        hashed_password = bcrypt.generate_password_hash(form.get('password')).decode('utf-8')
        register = Users(
            Fullnames = form.get('full_names'),
            Email = form.get('email_address'),
            Phone = form.get('phone_number'),
            PostalAddress = form.get('postal_address'),
            PhysicalAddress = form.get('physical_address'),
            County = form.get('county'),
            DOB = form.get('dob'),
            Username = form.get('username'),
            Password = hashed_password
        )
        db.session.add(register)
        db.session.flush()
        db.session.commit()