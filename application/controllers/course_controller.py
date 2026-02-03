from flask import Blueprint, render_template, redirect, url_for, request, flash
from application.services.course_service import Course_service
from flask_login import login_required, current_user

course_ctr = Blueprint('course_ctr', __name__)
courseService = Course_service()

@course_ctr.route("/", methods=['GET','POST'])
@login_required
def Index_Page():
    if request.method == 'GET':
        courses = courseService.getAllCourse()
        return render_template("course.html", courses = courses)

    if request.method == 'POST':
        data = request.form
        courseService.createCourse(data)
        flash(f'successfully created course ({data.get("Name")}) record', 'success')
        return redirect(url_for('course_ctr.Index_Page'))

@course_ctr.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_pages(id):
    course = courseService.getCoursePerId(id)
    if request.method == 'GET':
        return render_template("edit_modal.html", course = course)

    if request.method == 'POST':
        data = request.form
        courseService.editCourse(id, data)
        flash(f'successfully updated course details ({course.Name}).', 'success')
        return redirect(url_for('course_ctr.Index_Page'))

@course_ctr.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_pages(id):
    course = courseService.getCoursePerId(id)
    if request.method == 'GET':
        return render_template("delete_modal.html",  course = course)

    if request.method == 'POST':
        courseService.deleteCourse(id)
        flash(f'course ({course.Name}) record successfully deleted', 'success')
        return redirect(url_for('course_ctr.Index_Page'))
