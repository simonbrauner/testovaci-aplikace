from config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    parts = db.Column(db.Integer, default=0)
    solution = db.Column(db.Boolean, default=1)
    access = db.Column(db.Boolean, default=0)

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


class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    test_id = db.Column(db.Integer, db.ForeignKey('test.id'),
                        nullable=False)
    test = db.relationship('Test', backref='submits')

    taker_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                         nullable=False)
    taker = db.relationship('User', backref='submits')

    score = db.Column(db.Integer, nullable=True)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    submit_id = db.Column(db.Integer, db.ForeignKey('submit.id'),
                          nullable=False)
    submit = db.relationship('Submit', backref='responses')

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)
    question = db.relationship('Question')

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'),
                          nullable=True)
    answer = db.relationship('Answer')


if __name__ == '__main__':
    db.create_all()
