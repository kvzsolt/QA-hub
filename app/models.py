from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.Date)
    number_of_asked_questions = db.Column(db.Integer)
    number_of_answers = db.Column(db.Integer)
    number_of_comments = db.Column(db.Integer)
    reputation = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.username}>'


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    submission_time = db.Column(db.DateTime)
    view_number = db.Column(db.Integer)
    vote_number = db.Column(db.Integer)
    title = db.Column(db.Text)
    message = db.Column(db.Text)
    image = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='question', cascade="all, delete-orphan")
    tags = db.relationship('Tag', secondary='question_tag', back_populates='questions')

    def __repr__(self):
        return f'<Question {self.title}>'


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    submission_time = db.Column(db.DateTime)
    vote_number = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    message = db.Column(db.Text)
    image = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_answer_accepted = db.Column(db.Integer)

    question = db.relationship('Question', back_populates='answers')
    user = db.relationship('User', back_populates='answers')
    comments = db.relationship('Comment', back_populates='answer', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Answer {self.message}>'


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    message = db.Column(db.Text)
    submission_time = db.Column(db.DateTime)
    edited_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    question = db.relationship('Question', back_populates='comments')
    answer = db.relationship('Answer', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.message}>'


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    questions = db.relationship('Question', secondary='question_tag', back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.name}>'


class QuestionTag(db.Model):
    __tablename__ = 'question_tag'

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

    question = db.relationship('Question', back_populates='tags')
    tag = db.relationship('Tag', back_populates='questions')


User.questions = db.relationship('Question', order_by=Question.id, back_populates='user')
User.answers = db.relationship('Answer', order_by=Answer.id, back_populates='user')
User.comments = db.relationship('Comment', order_by=Comment.id, back_populates='user')

Question.tags = db.relationship('QuestionTag', back_populates='question')
Tag.questions = db.relationship('QuestionTag', back_populates='tag')
