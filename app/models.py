from app import db

class Task(db.Model):
    __tablename__ = "task"  # lowercase

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="pending")

class User(db.Model):
    __tablename__ = "user"  # lowercase
    id = db.Column(db.Integer , primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # bigger for hashed pw
