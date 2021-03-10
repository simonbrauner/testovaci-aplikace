from flask_sqlalchemy import SQLAlchemy

from tools import create_app

app = create_app()

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


if __name__ == '__main__':
    db.create_all()
