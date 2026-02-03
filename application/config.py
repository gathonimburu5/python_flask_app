from urllib.parse import quote
import secrets

class Config():
    HOST = "0.0.0.0"
    DB_USERNAME = "postgres"
    DB_PASSWORD = quote("@Paulmburu5")
    # POSTGRES_URL = "127.0.0.1"
    POSTGRES_URL = "book_db"
    POSTGRES_DB = "SkoteDb"
    POSTGRES_PORT = 5432
    DB_URL = 'postgresql://{user}:{pswd}@{url}:{port}/{db}?application_name=skoteApp'.format(user=DB_USERNAME, pswd=DB_PASSWORD, url=POSTGRES_URL, port=POSTGRES_PORT, db=POSTGRES_DB)

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_BINDS = { 'SkoteDb':DB_URL }
    
    SECRET_KEY = secrets.token_hex(16)
    SECURITY_PASSWORD_SALT = secrets.token_hex(30)

    DEFAULT_PROFILE_IMAGE = "default1.png"
    DEFAULT_STUDENT_PROFILE = "defaultIcon.png"
    
    # mail configuration
    MAIL_SERVER = "smtp.ethereal.email"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "aisha.paucek@ethereal.email"
    MAIL_PASSWORD = "79fQ9yzH8HMgepHsxT"


class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass

