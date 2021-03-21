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


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    test_id = db.Column(db.Integer, db.ForeignKey('test.id'),
                        nullable=False)
    test = db.relationship('Test', backref='questions')


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)
    question = db.relationship('Question', backref='answers')


if __name__ == '__main__':
    db.create_all()
