from application.extension import db
from application.models import Course

class Course_service():
    def getAllCourse(self):
        return Course.query.all()

    def createCourse(self, data):
        new_course = Course(
            Code = data.get('Code'),
            Name = data.get('Name')
        )
        db.session.add(new_course)
        db.session.commit()

    def getCoursePerId(self, id):
        return Course.query.get_or_404(id)

    def editCourse(self, id, data):
        course_to_edit = Course.query.get_or_404(id)
        course_to_edit.Code = data.get('Code')
        course_to_edit.Name = data.get('Name')

        db.session.commit()

    def deleteCourse(self, id):
        course_to_delete = Course.query.get_or_404(id)
        db.session.delete(course_to_delete)
        db.session.commit()

