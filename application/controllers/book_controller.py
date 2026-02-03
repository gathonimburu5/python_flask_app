from flask import Blueprint, request, render_template, redirect, url_for, flash
from application.services.book_service import BookService
from flask_login import login_required, current_user

book_ctrl = Blueprint('book_ctrl', __name__)
bookService = BookService()

@book_ctrl.route("/", methods=['GET', 'POST'])
@login_required
def Book_Page():
    # form = BookForm()
    # courses = bookService.getCourseList()
    # form.course.choices = [(course.Id, course.Name) for course in courses]

    if request.method == "GET":
        books = bookService.gettingAllBooks()
        courses = bookService.getCourseList()
        return render_template('book.html', books=books, courses=courses)

    if request.method == "POST":
        data = request.form
        bookService.createBook(data)
        flash(f'successfully created book ({data.get("book_tittle")})', 'success')
        return redirect(url_for('book_ctrl.Book_Page'))

@book_ctrl.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def Book_Edit(id):
    book = bookService.getBooksPerId(id)
    if request.method == "GET":
        courses = bookService.getCourseList()
        return render_template("update_modal.html", book=book, courses=courses)

    if request.method == "POST":
        data = request.form
        bookService.editBooks(id, data)
        flash(f'successfully updated books ({data.get("book_tittle")}) records', 'success')
        return redirect(url_for("book_ctrl.Book_Page"))

@book_ctrl.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_book_page(id):
    book = bookService.getBooksPerId(id)
    if request.method == "GET":
        return render_template("delete_modal.html", book=book)
    
    if request.method == "POST":
        bookService.deleteBooks(id)
        flash(f'successfully deleted {book.Tittle}', 'success')
        return redirect(url_for('book_ctrl.Book_Page'))