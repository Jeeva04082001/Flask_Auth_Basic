class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:123456@localhost:3306/flask_auth_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False