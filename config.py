class Config:
    SECRET_KEY = "nahtzm1z3n"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:12345678@cloud-data-storage-db.cttzyltmaz5j.us-east-1.rds.amazonaws.com/cloud-data-storage"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()
