from datetime import datetime
from app import db
from models import User, Question, Answer, Comment, Tag, QuestionTag

DATE_TIME_FORMAT = "%Y-%m-%d, %H:%M"


def get_questions():
    return Question.query.order_by(Question.id).all()


def add_new_question(new_question, user_id):
    timestamp = datetime.now().strftime(DATE_TIME_FORMAT)
    question = Question(
        submission_time=timestamp,
        view_number=0,
        vote_number=0,
        title=new_question['title'],
        message=new_question['message'],
        image=new_question['image'],
        user_id=user_id
    )
    db.session.add(question)
    db.session.commit()


def add_new_answer(new_answer, user_id):
    timestamp = datetime.now().strftime(DATE_TIME_FORMAT)
    answer = Answer(
        submission_time=timestamp,
        vote_number=0,
        question_id=new_answer['question_id'],
        message=new_answer['message'],
        image=new_answer['image'],
        user_id=user_id,
        is_answer_accepted=0
    )
    db.session.add(answer)
    db.session.commit()


def get_specific_question(question_id):
    return Question.query.get(question_id)


def delete_specific_question(question_id):
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()


def edit_specific_question(question_id, title, message, image):
    question = Question.query.get(question_id)
    if question:
        question.title = title
        question.message = message
        question.image = image
        db.session.commit()


def get_question_id_for_answer(answer_id):
    answer = Answer.query.get(answer_id)
    return answer.question_id if answer else None


def delete_specific_answer(answer_id):
    Answer.query.filter_by(id=answer_id).delete()
    db.session.commit()


def get_answers_for_specific_question(question_id):
    return Answer.query.filter_by(question_id=question_id).order_by(Answer.id).all()


def count_question_views(question_id):
    question = Question.query.get(question_id)
    if question:
        question.view_number += 1
        db.session.commit()


def question_count_votes(question_id, vote):
    question = Question.query.get(question_id)
    if question:
        question.vote_number += vote
        db.session.commit()


def count_answer_votes(answer_id, vote):
    answer = Answer.query.get(answer_id)
    if answer:
        answer.vote_number += vote
        db.session.commit()


def order_by(order_by, order_direction):
    return Question.query.order_by(db.text(f'{order_by} {order_direction}')).all()


def answers_order_by(order_by, order_direction):
    return Answer.query.order_by(db.text(f'{order_by} {order_direction}')).all()


def get_question_comment(question_id):
    return Comment.query.filter_by(question_id=question_id).all()


def get_all_comment_for_print():
    return Comment.query.all()


def add_new_question_comment(new_comment, question_id, user_id):
    timestamp = datetime.now().strftime(DATE_TIME_FORMAT)
    comment = Comment(
        question_id=question_id,
        message=new_comment,
        submission_time=timestamp,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()


def add_new_answer_comment(new_comment, answer_id, user_id):
    timestamp = datetime.now().strftime(DATE_TIME_FORMAT)
    comment = Comment(
        answer_id=answer_id,
        message=new_comment,
        submission_time=timestamp,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()


def find_question(search):
    return Question.query.filter(Question.title.ilike(f'%{search}%')).order_by(Question.id).all()


def edit_answer(answer_id, message, image):
    answer = Answer.query.get(answer_id)
    if answer:
        answer.message = message
        answer.image = image
        db.session.commit()


def get_specific_answer(answer_id):
    return Answer.query.get(answer_id)


def get_answers():
    return Answer.query.all()


def get_first_five_questions():
    return Question.query.order_by(Question.id.desc()).limit(5).all()


def delete_question_comment(comment_id):
    Comment.query.filter_by(id=comment_id).delete()
    db.session.commit()


def delete_answer_comment(comment_id):
    Comment.query.filter_by(id=comment_id).delete()
    db.session.commit()


def get_answer_id_for_comment(comment_id):
    comment = Comment.query.get(comment_id)
    return comment.answer.question_id if comment and comment.answer else None


def get_question_id_for_comment(comment_id):
    comment = Comment.query.get(comment_id)
    return comment.question_id if comment else None


def get_all_users_for_login():
    return User.query.all()


def get_users_for_login(user_name):
    return User.query.filter_by(email=user_name).first()


def get_password_for_login(email):
    user = User.query.filter_by(email=email).first()
    return user.password if user else None


def add_user(username, password):
    user = User(
        email=username,
        password=password,
        registration_date=datetime.now(),
        number_of_asked_questions=0,
        number_of_answers=0,
        number_of_comments=0,
        reputation=0
    )
    db.session.add(user)
    db.session.commit()


def list_all_users():
    return User.query.all()


def get_specific_user(user_id):
    return User.query.get(user_id)


def get_user_id_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user.id if user else None


def get_specific_user_questions(user_id):
    return Question.query.filter_by(user_id=user_id).all()


def get_specific_user_answers(user_id):
    return Answer.query.filter_by(user_id=user_id).all()


def get_specific_user_comments(user_id):
    return Comment.query.filter_by(user_id=user_id).all()


def add_tag(question_id, tag_id):
    question_tag = QuestionTag(question_id=question_id, tag_id=tag_id)
    db.session.add(question_tag)
    db.session.commit()


def get_tags():
    return Tag.query.all()


def add_new_tag(tag):
    new_tag = Tag(name=tag)
    db.session.add(new_tag)
    db.session.commit()


def get_tag_id(tag):
    tag = Tag.query.filter_by(name=tag).first()
    return tag.id if tag else None


def delete_tag(question_id, tag_id):
    QuestionTag.query.filter_by(question_id=question_id, tag_id=tag_id).delete()
    db.session.commit()


def get_tags_for_question(question_id):
    return Tag.query.join(QuestionTag).filter(QuestionTag.question_id == question_id).all()


def get_tags_with_num_of_use():
    return db.session.query(Tag.name, db.func.count(QuestionTag.question_id).label('num_of_use')).outerjoin(
        QuestionTag).group_by(Tag.id).all()


def accept_answer(answer_id, accepted_data):
    answer = Answer.query.get(answer_id)
    if answer:
        answer.is_answer_accepted = accepted_data
        db.session.commit()


def get_user_id_by_question_id(question_id):
    question = Question.query.get(question_id)
    return question.user_id if question else None


def count_reputation(reputation, user_id):
    user = User.query.get(user_id)
    if user:
        user.reputation += reputation
        db.session.commit()
