from sqlalchemy import text
from application.extension import db, app
from application.models import Book, Course
from flask import request
import os, uuid
from werkzeug.utils import secure_filename

class BookService():
    def getAllBooks(self):
        books = db.session.query(Book, Course).join(Course, Book.CourseId == Course.Id).all()
        return books

    def gettingAllBooks(self):
        books = Book.query.join(Course, Book.CourseId == Course.Id)\
        .add_columns(Book.Id, Book.Tittle, Book.Author, Book.ISBN, Book.PublishedOn, Book.CourseId, Course.Code, Course.Name, Book.BookPoster, Book.CreatedOn).order_by(Book.Id.asc()).all()
        return books

    def getBooksPerId(self, id):
        book = Book.query.join(Course, Book.CourseId==Course.Id)\
        .add_columns(Book.Id, Book.Tittle, Book.Author, Book.ISBN, Book.PublishedOn, Book.CourseId, Course.Code, Course.Name, Book.BookPoster, Book.CreatedOn).filter(Book.Id==id).one_or_none()
        return book

    def getCourseList(self):
        course = Course.query.add_columns(Course.Id, Course.Code, Course.Name, Course.CreatedOn).all()
        return course

    def createBook(self, form):
        poster = request.files.get("book_poster")
        if poster:
            book_poster = f"{uuid.uuid4().hex}{os.path.splitext(poster.filename)[1]}"
            book_poster = secure_filename(book_poster)
            book_url = os.path.join(app.root_path, 'static/assets/BookPoster/', book_poster)
            poster.save(book_url)
        else:
            book_poster = "default1.png"

        new_book = Book(
            Tittle = form.get("book_tittle"),
            Author = form.get("book_author"),
            ISBN = form.get("book_isbn"),
            PublishedOn = form.get("published_on"),
            CourseId = form.get("course_id"),
            BookPoster = book_poster
        )
        db.session.add(new_book)
        db.session.flush()
        db.session.commit()

    def editBooks(self, id, form):
        book_update = Book.query.filter(Book.Id == id).one_or_404()
        poster = request.files.get("book_poster")
        if poster:
            book_poster = f"{uuid.uuid4().hex}{os.path.splitext(poster.filename)[1]}"
            book_poster = secure_filename(book_poster)
            book_url = os.path.join(app.root_path, 'static/assets/BookPoster/', book_poster)
            poster.save(book_url)

        book_update.Tittle = form.get("book_tittle")
        book_update.Author = form.get("book_author")
        book_update.ISBN = form.get("book_isbn")
        book_update.PublishedOn = form.get("published_on")
        book_update.CourseId = form.get("course_id")
        book_update.BookPoster = book_poster
        db.session.flush()
        db.session.commit()

    def deleteBooks(self, id):
        book_delete = Book.query.filter(Book.Id == id).one_or_404()
        db.session.delete(book_delete)
        db.session.commit()
