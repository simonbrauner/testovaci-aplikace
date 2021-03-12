from config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    creator = db.relationship('User', backref='tests', lazy=True)


if __name__ == '__main__':
    db.create_all()
