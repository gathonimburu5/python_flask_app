from application.extension import db, app
from flask import request
import os, uuid
from werkzeug.utils import secure_filename
from sqlalchemy import text
from application.models import Student, Course

class Student_Service():
    def getStudents(self):
        students = db.session.query(Student, Course).join(Course, Student.CourseId == Course.Id).all()
        return students

    def gettingAllStudent(self):
        students = Student.query.join(Course, Student.CourseId == Course.Id)\
        .add_columns(Student.Id, Student.AdmNo, Student.FullNames, Student.EmailAddress, Student.PhoneNumber, Student.County, Student.CourseId, Course.Code, Course.Name, Student.StudentProfile, Student.CreatedOn).order_by(Student.Id.asc()).all()
        return students

    def getAllStudent(self):
        stude_query = text(""" SELECT a.*, b."Code", b."Name" FROM "student" a LEFT JOIN "course" b on b."Id" = a."CourseId" ORDER BY a."Id" ASC; """)
        with db.engine.connect() as con:
            students = con.execute(stude_query).fetchall()
            con.close()
        return students

    def getCourseList(self):
        return Course.query.all()

    def createStudent(self, data):
        profile = request.files.get("student_profile")
        if profile:
            picture_name = f"{uuid.uuid4().hex}{os.path.splitext(profile.filename)[1]}"
            picture_name = secure_filename(picture_name)
            picture_url = os.path.join(app.root_path, 'static/assets/profile/', picture_name)
            profile.save(picture_url)
        else:
            picture_name = "defaultIcon.png"

        new_student = Student(
            AdmNo = data.get('AdmNo'),
            FullNames = data.get('FullNames'),
            EmailAddress = data.get('EmailAddress'),
            PhoneNumber = data.get('PhoneNumber'),
            County = data.get('County'),
            CourseId = data.get('CourseId'),
            StudentProfile = picture_name
        )
        db.session.add(new_student)
        db.session.flush()
        db.session.commit()

    def getStudentPerId(self, id):
        #student = Student.query.get_or_404(id)
        student = Student.query.join(Course, Student.CourseId == Course.Id)\
        .add_columns(Student.Id, Student.AdmNo, Student.FullNames, Student.EmailAddress, Student.PhoneNumber, Student.County, Student.CourseId, Course.Code, Course.Name, Student.StudentProfile, Student.CreatedOn)\
        .filter(Student.Id == id).one_or_none()
        return student

    def editStudent(self, id, data):
        student_edit = Student.query.filter(Student.Id == id).one_or_404()
        profile = request.files.get('student_profile')
        if profile:
            pic_name = f"{uuid.uuid4().hex}{os.path.splitext(profile.filename)[1]}"
            pic_name = secure_filename(pic_name)
            pi_url = os.path.join(app.root_path, 'static/assets/profile/', pic_name)
            profile.save(pi_url)

        student_edit.AdmNo = data.get('AdmNo')
        student_edit.FullNames = data.get('FullNames')
        student_edit.EmailAddress = data.get('EmailAddress')
        student_edit.PhoneNumber = data.get('PhoneNumber')
        student_edit.County = data.get('County')
        student_edit.CourseId = data.get('CourseId')
        student_edit.StudentProfile = pic_name
        db.session.flush()
        db.session.commit()

    def deleteStudent(self, id):
        student_delete = Student.query.filter(Student.Id == id).one_or_404()
        db.session.delete(student_delete)
        db.session.commit()

