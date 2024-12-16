from flask import Flask
from application.extension import app, db, migrate, login, bcrypt, mail

def application_run():
    if app.config["DEBUG"] == "production":
        app.config.from_object("application.config.DevelopmentConfig")
    else:
        app.config.from_object("application.config.ProductionConfig")

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from application.controllers.book_controller import book_ctrl
    app.register_blueprint(book_ctrl, url_prefix="/book")

    from application.controllers.student_controller import student_ctrl
    app.register_blueprint(student_ctrl, url_prefix="/student")

    from application.controllers.course_controller import course_ctr
    app.register_blueprint(course_ctr, url_prefix="/course")

    from application.controllers.dashboard_controller import dash_ctrl
    app.register_blueprint(dash_ctrl, url_prefix="/dashboard")

    from application.controllers.auth_controller import auth_ctl
    app.register_blueprint(auth_ctl, url_prefix="/")

    return app

