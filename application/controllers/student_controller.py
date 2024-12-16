from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from application.models import load_tokens, Student
from application.services.student_service import Student_Service
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid
from application.extension import db, app

student_ctrl = Blueprint('student_ctrl', __name__)
studentService = Student_Service()

# @student_ctrl.before_request
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


@student_ctrl.route("/", methods=['GET', 'POST'])
@login_required
def Student_Page():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_ctl.login_page'))

    if request.method == "GET":
        students = studentService.gettingAllStudent()
        courses = studentService.getCourseList()
        return render_template('student.html', students=students, courses=courses)

    if request.method == "POST":
        data = request.form

        check_exit = Student.query.filter((Student.AdmNo == data.get('AdmNo')) | (Student.EmailAddress == data.get('EmailAddress'))).first()
        if check_exit:
            flash(f"student admn no or email address already registered.", "error")
            return redirect(url_for('student_ctrl.Student_Page'))

        studentService.createStudent(data)
        flash(f"successfully created student record", "success")
        return redirect(url_for('student_ctrl.Student_Page'))

@student_ctrl.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def studentEdit_page(id):
    stude = studentService.getStudentPerId(id)
    print(stude.StudentProfile)
    if request.method == "GET":
        courses = studentService.getCourseList()
        return render_template("update_modal.html", stude=stude, courses=courses)

    if request.method == "POST":
        data = request.form
        studentService.editStudent(id, data)
        flash(f'successfully updated student record', 'success')
        return redirect(url_for('student_ctrl.Student_Page'))

@student_ctrl.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_student_page(id):
    student = studentService.getStudentPerId(id)
    if request.method == "GET":
        return render_template("delete_modal.html", student=student)

    if request.method == "POST":
        studentService.deleteStudent(id)
        flash(f'successfully deleted {student.FullNames}', 'success')
        return redirect(url_for('student_ctrl.Student_Page'))
